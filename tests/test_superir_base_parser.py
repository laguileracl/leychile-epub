"""
Tests unitarios para el parser base de documentos SUPERIR.

Author: Luis Aguilera Arteaga <luis@aguilera.cl>
"""


from leychile_epub.superir_base_parser import (
    PATRON_FECHA,
    PATRON_LEY_REF,
    PATRON_RESOLUCION_EXENTA,
    SuperirBaseParser,
)

# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

SAMPLE_DOC = """RESOLUCIÓN EXENTA N.° 6597
MAT.: APRUEBA LA NORMA SOBRE FORMALIDADES
DE LAS PUBLICACIONES
SANTIAGO, 11 AGOSTO 2023

VISTOS:
Lo dispuesto en la Ley N° 20.720, que Sustituye el Régimen Concursal
vigente por una Ley de Reorganización y Liquidación de Activos de
Empresas y Personas, y en la Ley N° 21.563.

CONSIDERANDO:
Que el artículo 331 de la Ley N° 20.720 faculta a esta Superintendencia
para dictar normas de carácter general.

RESUELVO:

TÍTULO I
DISPOSICIONES GENERALES

Artículo 1. Objeto. La presente norma regula las formalidades.

Artículo 2. Ámbito de aplicación. Esta norma se aplica a todos los
procedimientos concursales.

TÍTULO II
REQUISITOS ESPECÍFICOS

Artículo 3. Los interesados deberán presentar la solicitud.

Artículo transitorio. Las disposiciones de esta norma entrarán en vigencia
a contar de su publicación.

II. NOTIFÍQUESE a los interesados.
III. PUBLÍQUESE en el Boletín Concursal.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS DE PATRONES REGEX
# ═══════════════════════════════════════════════════════════════════════════════


class TestPatterns:
    def test_fecha_with_de(self):
        m = PATRON_FECHA.search("Santiago, 11 de agosto de 2023")
        assert m
        assert m.group(1) == "11"
        assert m.group(2) == "agosto"
        assert m.group(3) == "2023"

    def test_fecha_without_de(self):
        m = PATRON_FECHA.search("SANTIAGO, 04 SEPTIEMBRE 2024")
        assert m
        assert m.group(1) == "04"
        assert m.group(2) == "SEPTIEMBRE"
        assert m.group(3) == "2024"

    def test_resolucion_exenta(self):
        m = PATRON_RESOLUCION_EXENTA.search("RESOLUCIÓN EXENTA N.° 6597")
        assert m
        assert m.group(1) == "6597"

    def test_resolucion_exenta_sin_punto(self):
        m = PATRON_RESOLUCION_EXENTA.search("RESOLUCION EXENTA N° 22802")
        assert m
        assert m.group(1) == "22802"

    def test_ley_ref(self):
        refs = PATRON_LEY_REF.findall("Ley N° 20.720 y Ley N° 21.563")
        assert len(refs) == 2
        assert "20.720" in refs
        assert "21.563" in refs


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS DEL PARSER BASE
# ═══════════════════════════════════════════════════════════════════════════════


class TestSuperirBaseParser:
    """Tests para SuperirBaseParser usando el parser directamente."""

    def setup_method(self):
        # Usar el parser base directamente (sin subclase)
        # pero necesitamos un patrón de número
        self.parser = SuperirBaseParser()
        # Override para tests: aceptar cualquier número
        import re

        self.parser.PATRON_NUMERO = re.compile(r"N[.°º]*\s*(\d+)")
        self.parser.TIPO_NORMA = "Test"
        self.parser.ID_PREFIX = "TEST"

    def test_extract_metadata_fecha(self):
        metadata = self.parser._extract_metadata(SAMPLE_DOC)
        assert metadata.fecha_iso == "2023-08-11"
        assert "agosto" in metadata.fecha_texto

    def test_extract_metadata_resolucion(self):
        metadata = self.parser._extract_metadata(SAMPLE_DOC)
        assert metadata.resolucion_exenta == "6597"

    def test_extract_metadata_materia(self):
        metadata = self.parser._extract_metadata(SAMPLE_DOC)
        assert "FORMALIDADES" in metadata.materia.upper()
        assert "PUBLICACIONES" in metadata.materia.upper()

    def test_extract_law_references(self):
        refs = self.parser._extract_law_references(SAMPLE_DOC)
        assert "Ley 20.720" in refs
        assert "Ley 21.563" in refs

    def test_extract_dfl_references(self):
        text_with_dfl = SAMPLE_DOC + "\nD.F.L. N° 1-19.653 de 2001."
        refs = self.parser._extract_law_references(text_with_dfl)
        dfl_refs = [r for r in refs if r.startswith("DFL")]
        assert len(dfl_refs) >= 1

    def test_extract_ds_references(self):
        text_with_ds = SAMPLE_DOC + "\nDecreto Supremo N° 181 de 2022."
        refs = self.parser._extract_law_references(text_with_ds)
        assert "D.S. 181" in refs

    def test_extract_ncg_references(self):
        text_with_ncg = SAMPLE_DOC + "\nNorma de Carácter General N° 14."
        refs = self.parser._extract_law_references(text_with_ncg)
        assert "NCG 14" in refs

    def test_split_sections_vistos(self):
        sections = self.parser._split_sections(SAMPLE_DOC)
        assert "Ley N° 20.720" in sections["vistos"]

    def test_split_sections_considerando(self):
        sections = self.parser._split_sections(SAMPLE_DOC)
        assert "artículo 331" in sections["considerando"]

    def test_split_sections_body(self):
        sections = self.parser._split_sections(SAMPLE_DOC)
        assert "Artículo 1" in sections["body"]

    def test_split_sections_closing(self):
        sections = self.parser._split_sections(SAMPLE_DOC)
        assert "NOTIFÍQUESE" in sections["closing"]

    def test_parse_body_articles(self):
        sections = self.parser._split_sections(SAMPLE_DOC)
        estructuras = self.parser._parse_body(sections["body"])
        n_arts = self.parser._count_articles(estructuras)
        assert n_arts == 4  # 3 regular + 1 transitorio

    def test_parse_body_divisions(self):
        sections = self.parser._split_sections(SAMPLE_DOC)
        estructuras = self.parser._parse_body(sections["body"])
        n_divs = self.parser._count_divisions(estructuras)
        assert n_divs == 2  # 2 títulos

    def test_parse_body_transitorio(self):
        sections = self.parser._split_sections(SAMPLE_DOC)
        estructuras = self.parser._parse_body(sections["body"])
        # Find transitorio article
        transitorios = []
        for e in estructuras:
            for h in e.hijos:
                if h.transitorio:
                    transitorios.append(h)
            if e.transitorio:
                transitorios.append(e)
        assert len(transitorios) == 1
        assert transitorios[0].nombre_parte == "transitorio"

    def test_parse_full(self):
        norma = self.parser.parse(SAMPLE_DOC, url="https://example.com/test.pdf")
        assert norma.norma_id.startswith("TEST-")
        assert norma.identificador.tipo == "Test"
        assert len(norma.estructuras) > 0

    def test_parse_with_catalog(self):
        catalog = {
            "materias": ["Publicaciones", "Formalidades"],
            "nombres_comunes": ["Test NCG"],
            "resolucion_exenta": "6597",
        }
        norma = self.parser.parse(SAMPLE_DOC, catalog_entry=catalog)
        assert "Publicaciones" in norma.metadatos.materias
        assert "Formalidades" in norma.metadatos.materias
        assert "Test NCG" in norma.metadatos.nombres_uso_comun

    def test_capitalize_materia_allcaps(self):
        result = SuperirBaseParser._capitalize_materia("FORMALIDADES DE LAS PUBLICACIONES")
        assert result == "Formalidades de las publicaciones"

    def test_capitalize_materia_mixed(self):
        result = SuperirBaseParser._capitalize_materia("Formalidades de las Publicaciones")
        assert result == "Formalidades de las Publicaciones"

    def test_body_excludes_directives(self):
        sections = self.parser._split_sections(SAMPLE_DOC)
        assert "NOTIFÍQUESE" not in sections["body"]

    def test_encabezado_has_vistos_and_considerando(self):
        norma = self.parser.parse(SAMPLE_DOC)
        assert "VISTOS:" in norma.encabezado_texto
        assert "CONSIDERANDO:" in norma.encabezado_texto

    def test_promulgacion_has_closing(self):
        norma = self.parser.parse(SAMPLE_DOC)
        assert "NOTIFÍQUESE" in norma.promulgacion_texto

    def test_fuente_populated(self):
        norma = self.parser.parse(SAMPLE_DOC)
        assert "Superintendencia" in norma.metadatos.identificacion_fuente

    def test_numero_fuente_populated(self):
        norma = self.parser.parse(SAMPLE_DOC)
        assert norma.metadatos.numero_fuente == "6597"

    def test_leyes_referenciadas_in_norma(self):
        norma = self.parser.parse(SAMPLE_DOC)
        refs = norma.metadatos.leyes_referenciadas
        assert any("20.720" in r for r in refs)
        assert any("21.563" in r for r in refs)

    def test_leyes_referenciadas_has_entries(self):
        norma = self.parser.parse(SAMPLE_DOC)
        refs = norma.metadatos.leyes_referenciadas
        assert len(refs) >= 2  # Al menos Ley 20.720 y 21.563
