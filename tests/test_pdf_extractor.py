"""
Tests unitarios para el extractor de PDF.

Author: Luis Aguilera Arteaga <luis@aguilera.cl>
"""

import pytest

from leychile_epub.pdf_extractor import PDFTextExtractor


class TestPDFTextExtractorInit:
    """Tests para inicialización del extractor."""

    def test_init_default(self):
        ext = PDFTextExtractor()
        assert ext.cache_dir is None

    def test_init_with_cache_dir(self, tmp_path):
        ext = PDFTextExtractor(cache_dir=str(tmp_path / "cache"))
        assert ext.cache_dir is not None

    def test_init_without_pdfplumber(self, monkeypatch):
        import leychile_epub.pdf_extractor as mod

        monkeypatch.setattr(mod, "pdfplumber", None)
        with pytest.raises(ImportError, match="pdfplumber"):
            PDFTextExtractor()


class TestCleanText:
    """Tests para _clean_text."""

    def test_removes_control_chars(self):
        ext = PDFTextExtractor()
        cleaned = ext._clean_text("Hello\x00World\x0b\uffff")
        assert "\x00" not in cleaned
        assert "\uffff" not in cleaned
        assert "HelloWorld" in cleaned

    def test_fixes_hyphenated_words(self):
        ext = PDFTextExtractor()
        cleaned = ext._clean_text("reglamen-\ntación")
        assert "reglamentación" in cleaned

    def test_normalizes_line_endings(self):
        ext = PDFTextExtractor()
        cleaned = ext._clean_text("line1\r\nline2\rline3")
        assert "\r" not in cleaned
        assert "line1\nline2\nline3" in cleaned

    def test_removes_page_numbers(self):
        ext = PDFTextExtractor()
        cleaned = ext._clean_text("Texto antes\n  42  \nTexto después")
        # Page number 42 should be removed
        assert cleaned.count("42") == 0

    def test_collapses_blank_lines(self):
        ext = PDFTextExtractor()
        cleaned = ext._clean_text("A\n\n\n\n\nB")
        assert "\n\n\n" not in cleaned
        assert "A\n\nB" in cleaned

    def test_strips_trailing_spaces(self):
        ext = PDFTextExtractor()
        cleaned = ext._clean_text("line with spaces   \nnext line  ")
        for line in cleaned.split("\n"):
            assert line == line.rstrip()

    def test_removes_repeated_headers(self):
        ext = PDFTextExtractor()
        header = "SUPERINTENDENCIA DE INSOLVENCIA"
        text = "\n".join([
            header, "Artículo 1.", header, "Texto.", header, "Más texto.", header, "Final."
        ])
        cleaned = ext._clean_text(text)
        assert cleaned.count(header) == 1

    def test_preserves_section_markers(self):
        ext = PDFTextExtractor()
        text = "VISTOS:\nTexto\nVISTOS:\nMás"
        cleaned = ext._clean_text(text)
        # VISTOS: appears only twice, won't be treated as header
        assert "VISTOS:" in cleaned
