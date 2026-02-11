"""
Extractor de texto desde archivos PDF.

Descarga PDFs desde URLs y extrae su contenido textual usando pdfplumber.
Soporta detección automática de PDFs escaneados que requieren OCR.

Author: Luis Aguilera Arteaga <luis@aguilera.cl>
"""

import logging
import re
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests

logger = logging.getLogger("leychile_epub.pdf_extractor")

try:
    import pdfplumber
except ImportError:
    pdfplumber = None  # type: ignore[assignment]


class PDFExtractionError(Exception):
    """Error durante la extracción de texto de un PDF."""

    pass


class PDFTextExtractor:
    """Extrae texto de archivos PDF.

    Soporta PDFs digitales (extracción directa con pdfplumber)
    y detección de PDFs escaneados que requieren OCR manual.

    Example:
        >>> from leychile_epub.pdf_extractor import PDFTextExtractor
        >>> extractor = PDFTextExtractor(cache_dir="./pdfs")
        >>> texto, pdf_path = extractor.download_and_extract(
        ...     "https://www.superir.gob.cl/wp-content/uploads/2025/11/NCG-N°28.pdf"
        ... )
    """

    def __init__(self, cache_dir: str | Path | None = None) -> None:
        """Inicializa el extractor.

        Args:
            cache_dir: Directorio para cachear PDFs descargados.
                      Si es None, usa un directorio temporal.
        """
        if pdfplumber is None:
            raise ImportError(
                "pdfplumber es requerido para extracción de PDFs. "
                "Instalar con: pip install 'leychile-epub[pdf]'"
            )
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; LeyChile-ePub/1.6.0)"
        })

    def download(self, url: str, output_dir: str | Path | None = None) -> Path:
        """Descarga un PDF desde una URL.

        Args:
            url: URL del PDF.
            output_dir: Directorio de destino. Si es None, usa cache_dir o temp.

        Returns:
            Path al archivo PDF descargado.
        """
        if output_dir:
            dest = Path(output_dir)
        elif self.cache_dir:
            dest = self.cache_dir
        else:
            dest = Path(tempfile.mkdtemp(prefix="ncg_"))

        dest.mkdir(parents=True, exist_ok=True)

        # Extraer nombre de archivo de la URL
        parsed = urlparse(url)
        filename = unquote(Path(parsed.path).name)
        if not filename.endswith(".pdf"):
            filename += ".pdf"

        output_path = dest / filename

        # Saltar si ya está descargado
        if output_path.exists() and output_path.stat().st_size > 0:
            logger.info(f"PDF ya descargado: {output_path}")
            return output_path

        logger.info(f"Descargando: {url}")
        response = self._session.get(url, timeout=60, stream=True)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        size = output_path.stat().st_size
        logger.info(f"PDF guardado: {output_path.name} ({size:,} bytes)")
        return output_path

    def extract_text(self, pdf_path: Path) -> str:
        """Extrae texto de un archivo PDF.

        Args:
            pdf_path: Ruta al archivo PDF.

        Returns:
            Texto extraído y limpio.

        Raises:
            PDFExtractionError: Si no se puede extraer texto.
        """
        if not pdf_path.exists():
            raise PDFExtractionError(f"Archivo no encontrado: {pdf_path}")

        logger.info(f"Extrayendo texto de: {pdf_path.name}")

        pages_text = []
        empty_pages = 0

        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            logger.info(f"  {total_pages} páginas detectadas")

            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text and text.strip():
                    pages_text.append(text)
                else:
                    empty_pages += 1
                    logger.debug(f"  Página {i + 1}/{total_pages}: sin texto extraíble")

        if not pages_text:
            raise PDFExtractionError(
                f"No se pudo extraer texto de {pdf_path.name}. "
                f"El PDF tiene {total_pages} páginas pero ninguna tiene texto extraíble. "
                "Podría ser un PDF escaneado que requiere OCR."
            )

        if empty_pages > 0:
            logger.warning(
                f"  {empty_pages}/{total_pages} páginas sin texto "
                "(posiblemente imágenes o páginas en blanco)"
            )

        full_text = "\n\n".join(pages_text)
        cleaned = self._clean_text(full_text)

        logger.info(f"  Texto extraído: {len(cleaned):,} caracteres")
        return cleaned

    def download_and_extract(self, url: str) -> tuple[str, Path]:
        """Descarga un PDF y extrae su texto.

        Args:
            url: URL del PDF.

        Returns:
            Tupla (texto_extraído, ruta_pdf).
        """
        pdf_path = self.download(url)
        text = self.extract_text(pdf_path)
        return text, pdf_path

    def _clean_text(self, text: str) -> str:
        """Limpia el texto extraído de un PDF.

        - Normaliza saltos de línea
        - Elimina headers/footers repetidos
        - Corrige guiones de fin de línea
        - Normaliza espacios
        """
        # Eliminar caracteres inválidos para XML (control chars, surrogates, noncharacters)
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\ufffe\uffff]", "", text)

        # Corregir palabras cortadas por guión al final de línea
        text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

        # Normalizar saltos de línea
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Eliminar números de página sueltos
        text = re.sub(r"\n\s*\d{1,3}\s*\n", "\n", text)
        text = re.sub(r"\n\s*Página\s+\d+\s+de\s+\d+\s*\n", "\n", text)

        # Detectar y eliminar headers/footers repetidos
        lines = text.split("\n")
        line_counts: dict[str, int] = {}
        for line in lines:
            stripped = line.strip()
            if stripped and len(stripped) > 5:
                line_counts[stripped] = line_counts.get(stripped, 0) + 1

        # Líneas que aparecen más de 3 veces son probablemente headers/footers
        protected = {
            "VISTOS:", "VISTO:", "CONSIDERANDO:", "RESUELVO:",
            "VISTOS", "VISTO", "CONSIDERANDO", "RESUELVO",
        }
        header_lines = {
            line
            for line, count in line_counts.items()
            if count > 3 and line.upper() not in protected
        }

        if header_lines:
            first_seen: set[str] = set()
            cleaned_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped in header_lines:
                    if stripped not in first_seen:
                        first_seen.add(stripped)
                        cleaned_lines.append(line)
                    # Omitir duplicados de header/footer
                else:
                    cleaned_lines.append(line)
            lines = cleaned_lines

        text = "\n".join(lines)

        # Colapsar múltiples líneas en blanco
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Eliminar espacios al final de cada línea
        text = "\n".join(line.rstrip() for line in text.split("\n"))

        return text.strip()
