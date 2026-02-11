"""
Parser para Instructivos de la SUPERIR.

Convierte texto extraído de PDFs de Instructivos en objetos Norma
compatibles con el pipeline de generación XML/ePub.

Hereda la lógica compartida de SuperirBaseParser y agrega
patrones específicos para detección de Instructivos.

Author: Luis Aguilera Arteaga <luis@aguilera.cl>
"""

import re

from .scraper_v2 import Norma
from .superir_base_parser import SuperirBaseParser, SuperirDocMetadata

# ═══════════════════════════════════════════════════════════════════════════════
# PATRONES ESPECÍFICOS INSTRUCTIVOS
# ═══════════════════════════════════════════════════════════════════════════════

# Detecta: "INSTRUCTIVO SUPERIR N.° 1", "INSTRUCTIVO N° 3", "INSTRUCTIVO SIR N° 1"
PATRON_INSTRUCTIVO_NUMERO = re.compile(
    r"INSTRUCTIVO\s+(?:SUPERIR|SIR\.?|S\.?I\.?R\.?)\s*N[.°º]*\s*(\d+)",
    re.IGNORECASE,
)

# Alternativa: buscar en MAT/título "INSTRUCTIVO N° X"
PATRON_INSTRUCTIVO_NUMERO_ALT = re.compile(
    r"INSTRUCTIVO\s*N[.°º]*\s*(\d+)",
    re.IGNORECASE,
)


# ═══════════════════════════════════════════════════════════════════════════════
# PARSER INSTRUCTIVOS
# ═══════════════════════════════════════════════════════════════════════════════


class InstructivoParser(SuperirBaseParser):
    """Parser para Instructivos de la SUPERIR.

    Convierte texto plano de Instructivos en objetos Norma compatibles
    con LawXMLGenerator para generación de XML.

    Example:
        >>> from leychile_epub.instructivo_parser import InstructivoParser
        >>> parser = InstructivoParser()
        >>> norma = parser.parse(texto, url="https://...")
    """

    PATRON_NUMERO = PATRON_INSTRUCTIVO_NUMERO
    TIPO_NORMA = "Instructivo"
    ID_PREFIX = "INST"

    def _extract_metadata(self, texto: str) -> SuperirDocMetadata:
        """Extrae metadatos con fallback para variantes de instructivos."""
        metadata = super()._extract_metadata(texto)

        # Si no se encontró número con el patrón principal, intentar alternativa
        if not metadata.numero:
            header = texto[:3000]
            match = PATRON_INSTRUCTIVO_NUMERO_ALT.search(header)
            if match:
                metadata.numero = match.group(1)

        return metadata

    def parse(
        self,
        texto: str,
        url: str = "",
        doc_numero: str = "",
        catalog_entry: dict | None = None,
    ) -> Norma:
        """Parsea un texto de Instructivo y retorna un objeto Norma.

        Args:
            texto: Texto completo del Instructivo.
            url: URL de origen del PDF.
            doc_numero: Número/ID del instructivo (override).
            catalog_entry: Metadatos adicionales del catálogo.

        Returns:
            Objeto Norma con toda la estructura parseada.
        """
        return super().parse(texto, url=url, doc_numero=doc_numero, catalog_entry=catalog_entry)

    def _build_titulo(self, metadata: SuperirDocMetadata, catalog: dict) -> str:
        """Construye el título completo del Instructivo."""
        if catalog.get("titulo_completo"):
            return catalog["titulo_completo"]

        parts = [f"INSTRUCTIVO SUPERIR N°{metadata.numero}"]
        if metadata.materia:
            materia = self._capitalize_materia(metadata.materia)
            parts.append(materia)
        return " - ".join(parts)
