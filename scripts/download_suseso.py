#!/usr/bin/env python3
"""Descargador del Compendio de Normas SUSESO (Ley 18.833).

Descarga la estructura completa del compendio desde el sitio web de la SUSESO,
extrayendo el índice jerárquico y el contenido textual de cada punto.

Uso:
    python scripts/download_suseso.py                    # Descargar todo
    python scripts/download_suseso.py --libro 1          # Solo Libro I
    python scripts/download_suseso.py --solo-indice      # Solo índice, sin contenido
    python scripts/download_suseso.py --force             # Forzar re-descarga
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://www.suseso.cl/620/"
ROOT_URL = f"{BASE_URL}w3-propertyname-785.html"
OUTPUT_DIR = Path("biblioteca_suseso")
RATE_LIMIT = 0.5  # segundos entre requests


# ---------------------------------------------------------------------------
# Modelo de datos
# ---------------------------------------------------------------------------


@dataclass
class NodoCompendio:
    """Nodo en el árbol jerárquico del compendio."""

    numero: str  # "1.1.1"
    titulo: str  # "DEFINICIÓN"
    titulo_completo: str  # "1.1.1 DEFINICIÓN"
    url: str  # URL completa
    pvid: str  # ID de la página (ej: "596395")
    nivel: int  # Profundidad (0=libro, 1=título, ...)
    hijos: list[NodoCompendio] = field(default_factory=list)

    def total_nodos(self) -> int:
        """Cuenta total de nodos en el subárbol."""
        return 1 + sum(h.total_nodos() for h in self.hijos)

    def hojas(self) -> list[NodoCompendio]:
        """Retorna solo los nodos hoja (sin hijos)."""
        if not self.hijos:
            return [self]
        result: list[NodoCompendio] = []
        for h in self.hijos:
            result.extend(h.hojas())
        return result

    def todos(self) -> list[NodoCompendio]:
        """Retorna todos los nodos en orden de recorrido."""
        result = [self]
        for h in self.hijos:
            result.extend(h.todos())
        return result

    def to_dict(self) -> dict:
        """Serializa a dict para JSON (sin contenido)."""
        d: dict = {
            "numero": self.numero,
            "titulo": self.titulo,
            "titulo_completo": self.titulo_completo,
            "url": self.url,
            "pvid": self.pvid,
            "nivel": self.nivel,
        }
        if self.hijos:
            d["hijos"] = [h.to_dict() for h in self.hijos]
        return d


# ---------------------------------------------------------------------------
# HTTP Client
# ---------------------------------------------------------------------------


def crear_session() -> requests.Session:
    """Crea una sesión HTTP con retry y headers apropiados."""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update(
        {
            "User-Agent": "LeyChile-ePub-Generator/1.1.0 (compendio-suseso)",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "es-CL,es;q=0.9",
        }
    )
    return session


def fetch_page(session: requests.Session, url: str) -> BeautifulSoup:
    """Descarga y parsea una página HTML."""
    resp = session.get(url, timeout=30)
    resp.encoding = "utf-8"
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


# ---------------------------------------------------------------------------
# Parsing del índice
# ---------------------------------------------------------------------------


def _parse_numero_titulo(texto: str) -> tuple[str, str]:
    """Separa '1.1.1 DEFINICIÓN' en ('1.1.1', 'DEFINICIÓN')."""
    texto = texto.strip()
    # Patrón: número(s) separados por punto, luego espacio, luego título
    m = re.match(r"^([\d]+(?:\.[\d]+)*)\s+(.+)$", texto)
    if m:
        return m.group(1), m.group(2).strip()
    return "", texto


def _extraer_pvid(tag: Tag) -> str:
    """Extrae el pvid de las clases CSS de un <a>."""
    for cls in tag.get("class", []):
        if cls.startswith("pvid-"):
            return cls[5:]
    return ""


def parsear_indice_libro(soup: BeautifulSoup, libro_num: int) -> NodoCompendio | None:
    """Parsea el índice completo de un libro desde su página.

    El índice está en div.indice-compendio como <ul><li> anidados.
    Cada <a> tiene clases con pvid-{id} y el texto incluye numeración.
    """
    indice_div = soup.find("div", class_="indice-compendio")
    if not indice_div:
        return None

    # El primer <ul> tiene el libro como primer <li>
    ul_raiz = indice_div.find("ul")
    if not ul_raiz:
        return None

    li_libro = ul_raiz.find("li", recursive=False)
    if not li_libro:
        return None

    return _parsear_li(li_libro, nivel=0)


def _parsear_li(li: Tag, nivel: int) -> NodoCompendio | None:
    """Parsea recursivamente un <li> del índice."""
    a_tag = li.find("a", recursive=False)
    if not a_tag:
        return None

    texto_completo = a_tag.get_text(strip=True)
    numero, titulo = _parse_numero_titulo(texto_completo)
    pvid = _extraer_pvid(a_tag)
    href = a_tag.get("href", "")
    url = urljoin(BASE_URL, href)

    nodo = NodoCompendio(
        numero=numero,
        titulo=titulo,
        titulo_completo=texto_completo,
        url=url,
        pvid=pvid,
        nivel=nivel,
    )

    # Buscar <ul> hijo directo para subnodos
    ul_hijo = li.find("ul", recursive=False)
    if ul_hijo:
        for sub_li in ul_hijo.find_all("li", recursive=False):
            hijo = _parsear_li(sub_li, nivel=nivel + 1)
            if hijo:
                nodo.hijos.append(hijo)

    return nodo


# ---------------------------------------------------------------------------
# Extracción de contenido
# ---------------------------------------------------------------------------


def extraer_contenido(soup: BeautifulSoup, pvid: str) -> str:
    """Extrae el contenido textual propio de una página del compendio.

    El contenido está en div#eidox_descendientes_agrupados.
    Para nodos hoja, contiene solo su propio texto.
    Para nodos intermedios, contiene el texto de todos los descendientes,
    así que extraemos solo el contenido que pertenece al pvid actual.
    """
    desc = soup.find("div", id="eidox_descendientes_agrupados")
    if not desc:
        # Fallback: buscar en compendio_completo
        comp = soup.find("div", id="compendio_completo")
        if comp:
            return _extraer_texto_recuadro(comp)
        return ""

    # Buscar el div.grupo más específico para este pvid
    # El ID sigue el patrón: eidox_descendientes_agrupados_group_..._pvid_{pvid}
    grupo = None
    for div in desc.find_all("div", class_="grupo"):
        div_id = div.get("id", "")
        if div_id.endswith(f"pvid_{pvid}"):
            grupo = div

    if grupo:
        return _extraer_texto_de_grupo(grupo)

    # Fallback: si no encontramos grupo específico, buscar recuadros directos
    recuadros = desc.find_all("div", class_="recuadro", recursive=True)
    if len(recuadros) == 1:
        return _extraer_texto_recuadro(recuadros[0])

    return ""


def _extraer_texto_de_grupo(grupo: Tag) -> str:
    """Extrae texto de un div.grupo, excluyendo sub-grupos (hijos)."""
    partes: list[str] = []

    # Buscar recuadros directos de este grupo (no los de sub-grupos)
    for child in grupo.children:
        if not isinstance(child, Tag):
            continue
        if child.name == "div" and "recuadro" in child.get("class", []):
            texto = _extraer_texto_recuadro(child)
            if texto:
                partes.append(texto)
        # No descender en sub-grupos (class="grupo")

    return "\n\n".join(partes)


def _extraer_texto_recuadro(recuadro: Tag) -> str:
    """Extrae texto limpio de un div.recuadro."""
    partes: list[str] = []

    for elem in recuadro.descendants:
        if not isinstance(elem, Tag):
            continue

        # Saltar epígrafes (duplican el título)
        if "epigrafe" in " ".join(elem.get("class", [])):
            continue

        if elem.name == "p" and elem.parent and _es_contenido_directo(elem):
            texto = _get_text_with_spaces(elem)
            if texto:
                partes.append(texto)

        elif elem.name == "table":
            tabla_texto = _extraer_tabla(elem)
            if tabla_texto:
                partes.append(tabla_texto)

        elif elem.name in ("h2", "h3", "h4", "h5") and _es_contenido_directo(elem):
            texto = _get_text_with_spaces(elem)
            if texto and not any(texto in p for p in partes):
                partes.append(texto)

    # Deduplicar párrafos consecutivos idénticos
    resultado: list[str] = []
    for p in partes:
        if not resultado or p != resultado[-1]:
            resultado.append(p)

    # Separar "Referencias legales:" en su propia sección
    texto_final = "\n\n".join(resultado)
    texto_final = re.sub(
        r"(Referencias legales:)",
        r"\n\n\1\n",
        texto_final,
    )
    # Separar referencias individuales con guión
    texto_final = re.sub(r"-(?=(?:DFL|Ley|D\.?[SL]|Código|Art))", r"\n- ", texto_final)

    return texto_final.strip()


def _get_text_with_spaces(elem: Tag) -> str:
    """Extrae texto de un elemento, insertando espacios entre tags inline.

    BeautifulSoup's get_text() no agrega espacios entre <span> adyacentes,
    produciendo "artículo1° de la Ley". Esta función corrige eso.
    """
    parts: list[str] = []
    for child in elem.children:
        if isinstance(child, str):
            parts.append(child)
        elif isinstance(child, Tag):
            if child.name in ("br",):
                parts.append("\n")
            else:
                parts.append(child.get_text())
    text = " ".join(parts)
    # Limpiar espacios múltiples pero preservar saltos de línea
    text = re.sub(r"[^\S\n]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return text.strip()


def _es_contenido_directo(elem: Tag) -> bool:
    """Verifica que el elemento no esté dentro de un sub-grupo o epígrafe."""
    for parent in elem.parents:
        if not isinstance(parent, Tag):
            continue
        classes = parent.get("class", [])
        if "epigrafe" in " ".join(classes):
            return False
    return True


def _extraer_tabla(table: Tag) -> str:
    """Extrae una tabla como texto tabulado."""
    filas: list[str] = []
    for tr in table.find_all("tr"):
        celdas = []
        for td in tr.find_all(["td", "th"]):
            celdas.append(td.get_text(strip=True))
        if celdas:
            filas.append(" | ".join(celdas))
    return "\n".join(filas)


# ---------------------------------------------------------------------------
# Descubrimiento de libros
# ---------------------------------------------------------------------------

# Catálogo estático de libros (URLs descubiertas del sitio)
LIBROS_CATALOG: dict[int, dict[str, str]] = {
    1: {
        "titulo": "DESCRIPCIÓN GENERAL",
        "url": f"{BASE_URL}w3-propertyvalue-596393.html",
    },
    2: {
        "titulo": "AFILIACIÓN Y DESAFILIACIÓN",
        "url": f"{BASE_URL}w3-propertyvalue-605090.html",
    },
    3: {
        "titulo": "RÉGIMEN DE CRÉDITO SOCIAL",
        "url": f"{BASE_URL}w3-propertyvalue-593609.html",
    },
    4: {
        "titulo": "PRESTACIONES LEGALES Y DE BIENESTAR SOCIAL",
        "url": f"{BASE_URL}w3-propertyvalue-596430.html",
    },
    5: {
        "titulo": "ASPECTOS OPERACIONALES Y ADMINISTRATIVOS",
        "url": f"{BASE_URL}w3-propertyvalue-599745.html",
    },
    6: {
        "titulo": "GESTIÓN DE RIESGOS",
        "url": f"{BASE_URL}w3-propertyvalue-600694.html",
    },
    7: {
        "titulo": "ASPECTOS FINANCIERO CONTABLES",
        "url": f"{BASE_URL}w3-propertyvalue-615037.html",
    },
    8: {
        "titulo": "SISTEMAS DE INFORMACIÓN, INFORMES Y REPORTES",
        "url": f"{BASE_URL}w3-propertyvalue-608359.html",
    },
}


# ---------------------------------------------------------------------------
# Lógica principal de descarga
# ---------------------------------------------------------------------------


def _nombre_archivo(nodo: NodoCompendio) -> str:
    """Genera nombre de archivo a partir de número y título."""
    # Limpiar título para nombre de archivo
    titulo = nodo.titulo.lower()
    titulo = re.sub(r"[^\w\s-]", "", titulo)
    titulo = re.sub(r"\s+", "_", titulo.strip())
    titulo = titulo[:60]  # Truncar nombres largos
    if nodo.numero:
        return f"{nodo.numero}_{titulo}"
    return titulo


def descargar_libro(
    session: requests.Session,
    libro_num: int,
    output_dir: Path,
    solo_indice: bool = False,
    force: bool = False,
) -> NodoCompendio | None:
    """Descarga un libro completo del compendio."""
    info = LIBROS_CATALOG.get(libro_num)
    if not info:
        print(f"  ERROR: Libro {libro_num} no encontrado en catálogo")
        return None

    libro_dir = output_dir / f"libro_{libro_num}"
    libro_dir.mkdir(parents=True, exist_ok=True)

    # 1. Descargar página del libro y parsear índice
    print(f"\n{'='*60}")
    print(f"LIBRO {libro_num}: {info['titulo']}")
    print(f"{'='*60}")
    print(f"  Descargando índice desde {info['url']}")

    soup = fetch_page(session, info["url"])
    time.sleep(RATE_LIMIT)

    arbol = parsear_indice_libro(soup, libro_num)
    if not arbol:
        print("  ERROR: No se pudo parsear el índice")
        return None

    total = arbol.total_nodos()
    hojas = len(arbol.hojas())
    print(f"  Índice parseado: {total} nodos, {hojas} hojas")

    # 2. Guardar índice
    indice_path = libro_dir / "indice.json"
    with open(indice_path, "w", encoding="utf-8") as f:
        json.dump(arbol.to_dict(), f, ensure_ascii=False, indent=2)
    print(f"  Índice guardado: {indice_path}")

    if solo_indice:
        return arbol

    # 3. Descargar contenido de cada nodo
    todos_nodos = arbol.todos()
    descargados = 0
    saltados = 0

    for i, nodo in enumerate(todos_nodos):
        nombre = _nombre_archivo(nodo)
        txt_path = libro_dir / f"{nombre}.txt"

        # Skip si ya existe y no es force
        if txt_path.exists() and not force:
            saltados += 1
            continue

        # Fetch y extraer contenido
        try:
            soup_nodo = fetch_page(session, nodo.url)
            contenido = extraer_contenido(soup_nodo, nodo.pvid)
            time.sleep(RATE_LIMIT)
        except Exception as e:
            print(f"  ERROR [{nodo.numero}]: {e}")
            continue

        if contenido:
            # Escribir archivo con encabezado
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(f"{nodo.titulo_completo}\n")
                f.write(f"{'='*len(nodo.titulo_completo)}\n\n")
                f.write(contenido)
                f.write("\n")
            descargados += 1
        else:
            # Nodo estructural sin contenido propio - guardar solo título
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(f"{nodo.titulo_completo}\n")
                f.write(f"{'='*len(nodo.titulo_completo)}\n\n")
                f.write("(Nodo estructural - ver subnodos)\n")
            descargados += 1

        # Progreso
        progreso = (i + 1) / len(todos_nodos) * 100
        print(
            f"  [{progreso:5.1f}%] {nodo.numero} {nodo.titulo[:50]}"
            f" → {txt_path.name}"
        )

    print(f"\n  Resumen Libro {libro_num}:")
    print(f"    Descargados: {descargados}")
    print(f"    Saltados (ya existían): {saltados}")
    print(f"    Total nodos: {total}")

    return arbol


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Descarga el Compendio de Normas SUSESO (Ley 18.833)"
    )
    parser.add_argument(
        "--libro",
        type=int,
        nargs="*",
        help="Número(s) de libro a descargar (1-8). Sin argumento = todos.",
    )
    parser.add_argument(
        "--solo-indice",
        action="store_true",
        help="Solo descargar y guardar el índice, sin contenido.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Forzar re-descarga de archivos existentes.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_DIR,
        help=f"Directorio de salida (default: {OUTPUT_DIR})",
    )
    args = parser.parse_args()

    # Determinar qué libros descargar
    if args.libro:
        libros = args.libro
        for n in libros:
            if n not in LIBROS_CATALOG:
                print(f"Error: Libro {n} no existe. Disponibles: 1-8")
                sys.exit(1)
    else:
        libros = list(LIBROS_CATALOG.keys())

    output_dir: Path = args.output
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Compendio de Normas SUSESO - Ley 18.833")
    print(f"Libros a descargar: {libros}")
    print(f"Directorio de salida: {output_dir}")
    if args.solo_indice:
        print("Modo: solo índice")
    if args.force:
        print("Modo: forzar re-descarga")

    session = crear_session()
    arboles: dict[int, NodoCompendio] = {}

    for libro_num in libros:
        arbol = descargar_libro(
            session,
            libro_num,
            output_dir,
            solo_indice=args.solo_indice,
            force=args.force,
        )
        if arbol:
            arboles[libro_num] = arbol

    # Guardar índice general
    indice_general = {
        "compendio": "Compendio de Normas que regulan a las Cajas de Compensación de Asignación Familiar",
        "ley": "Ley 18.833",
        "fuente": ROOT_URL,
        "libros": {
            str(n): arbol.to_dict() for n, arbol in arboles.items()
        },
    }
    indice_path = output_dir / "indice_general.json"
    with open(indice_path, "w", encoding="utf-8") as f:
        json.dump(indice_general, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print("DESCARGA COMPLETADA")
    print(f"{'='*60}")
    print(f"Índice general: {indice_path}")
    total_nodos = sum(a.total_nodos() for a in arboles.values())
    print(f"Total nodos descargados: {total_nodos}")


if __name__ == "__main__":
    main()
