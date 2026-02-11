"""
LeyChile ePub Generator
=======================

Generador de libros electrónicos (ePub) y XML para legislación chilena.

Este paquete permite convertir leyes, decretos y otras normas de la
Biblioteca del Congreso Nacional de Chile en archivos ePub profesionales
y XML estructurado para agentes de IA.

Ejemplo de uso (v2 - recomendado):
    >>> from leychile_epub.scraper_v2 import BCNLawScraperV2
    >>> from leychile_epub.generator_v2 import EPubGeneratorV2
    >>> scraper = BCNLawScraperV2()
    >>> norma = scraper.scrape("https://www.leychile.cl/Navegar?idNorma=1058072")
    >>> generator = EPubGeneratorV2()
    >>> epub_path = generator.generate(norma, "output/ley.epub")

Ejemplo de uso XML (para agentes de IA):
    >>> from leychile_epub import LawXMLGenerator, BibliotecaXMLGenerator
    >>> generator = LawXMLGenerator()
    >>> xml_path = generator.generate_from_url(
    ...     "https://www.leychile.cl/Navegar?idNorma=172986",
    ...     output_dir="./biblioteca"
    ... )
    >>> # O generar biblioteca completa:
    >>> biblioteca = BibliotecaXMLGenerator()
    >>> resultado = biblioteca.generate(output_dir="./biblioteca_legal")

Ejemplo de uso (v1 - legacy):
    >>> from leychile_epub import BCNLawScraper, LawEpubGenerator
    >>> scraper = BCNLawScraper()
    >>> law_data = scraper.scrape_law("https://www.leychile.cl/Navegar?idNorma=242302")
    >>> generator = LawEpubGenerator()
    >>> epub_path = generator.generate(law_data)

Author: Luis Aguilera Arteaga <luis@aguilera.cl>
License: MIT
"""

__version__ = "1.6.0"
__author__ = "Luis Aguilera Arteaga"
__email__ = "luis@aguilera.cl"
__license__ = "MIT"

from .config import Config
from .exceptions import (
    GeneratorError,
    LeyChileError,
    NetworkError,
    ScraperError,
    ValidationError,
)
from .generator import LawEpubGenerator
from .instructivo_parser import InstructivoParser
from .ncg_parser import NCGParser
from .scraper import BCNLawScraper
from .superir_base_parser import SuperirBaseParser
from .xml_generator import (
    BibliotecaXMLGenerator,
    LawXMLGenerator,
    generate_law_xml,
    generate_library,
)

__all__ = [
    # Clases principales
    "BCNLawScraper",
    "LawEpubGenerator",
    "LawXMLGenerator",
    "BibliotecaXMLGenerator",
    "NCGParser",
    "InstructivoParser",
    "SuperirBaseParser",
    "Config",
    # Funciones de conveniencia
    "generate_law_xml",
    "generate_library",
    # Excepciones
    "LeyChileError",
    "ScraperError",
    "GeneratorError",
    "ValidationError",
    "NetworkError",
    # Metadata
    "__version__",
    "__author__",
    "__email__",
]
