"""
Parser para Normas de Carácter General (NCG) de la SUPERIR.

Convierte texto extraído de PDFs de NCG en objetos Norma
compatibles con el pipeline de generación XML/ePub.

Hereda la lógica compartida de SuperirBaseParser y agrega
patrones específicos para detección de NCGs.

Author: Luis Aguilera Arteaga <luis@aguilera.cl>
"""

import re

from .scraper_v2 import Norma
from .superir_base_parser import SuperirBaseParser, SuperirDocMetadata

# ═══════════════════════════════════════════════════════════════════════════════
# PATRONES ESPECÍFICOS NCG
# ═══════════════════════════════════════════════════════════════════════════════

PATRON_NCG_NUMERO = re.compile(
    r"(?:NCG|NORMA\s+DE\s+CAR[ÁA]CTER\s+GENERAL)\s*N\.?[°º]?\s*(\d+)",
    re.IGNORECASE,
)


# ═══════════════════════════════════════════════════════════════════════════════
# PARSER NCG
# ═══════════════════════════════════════════════════════════════════════════════


class NCGParser(SuperirBaseParser):
    """Parser para Normas de Carácter General de la SUPERIR.

    Convierte texto plano de NCGs en objetos Norma compatibles
    con LawXMLGenerator para generación de XML.

    Example:
        >>> from leychile_epub.ncg_parser import NCGParser
        >>> parser = NCGParser()
        >>> norma = parser.parse(texto_ncg, url="https://...")
    """

    PATRON_NUMERO = PATRON_NCG_NUMERO
    TIPO_NORMA = "Norma de Carácter General"
    ID_PREFIX = "NCG"

    def parse(
        self,
        texto: str,
        url: str = "",
        ncg_numero: str = "",
        catalog_entry: dict | None = None,
    ) -> Norma:
        """Parsea un texto de NCG y retorna un objeto Norma.

        Args:
            texto: Texto completo de la NCG.
            url: URL de origen del PDF.
            ncg_numero: Número de NCG (override si no se detecta del texto).
            catalog_entry: Metadatos adicionales del catálogo.

        Returns:
            Objeto Norma con toda la estructura parseada.
        """
        return super().parse(texto, url=url, doc_numero=ncg_numero, catalog_entry=catalog_entry)

    def _build_titulo(self, metadata: SuperirDocMetadata, catalog: dict) -> str:
        """Construye el título completo de la NCG."""
        # Usar título del catálogo si existe
        if catalog.get("titulo_completo"):
            return catalog["titulo_completo"]

        parts = [f"NORMA DE CARÁCTER GENERAL N°{metadata.numero}"]
        if metadata.materia:
            materia = self._capitalize_materia(metadata.materia)
            parts.append(materia)
        return " - ".join(parts)


def extract_ncg_number_from_url(url: str) -> str:
    """Extrae el número de NCG desde una URL de PDF.

    Args:
        url: URL del PDF (ej: ".../NCG-N°28.pdf")

    Returns:
        Número de NCG como string (ej: "28").
    """
    match = re.search(r"NCG[_\-\s]*N?[°º]?\s*(\d+)", url, re.IGNORECASE)
    if match:
        return match.group(1)
    return ""
