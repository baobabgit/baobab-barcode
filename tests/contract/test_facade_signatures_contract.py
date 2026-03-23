"""Contrat des signatures des fonctions de façade (package racine)."""

from __future__ import annotations

import inspect
from pathlib import Path

import baobab_barcode


class TestFacadeSignaturesContract:
    """Paramètres publics attendus des quatre fonctions de façade."""

    def test_validate_payload_signature(self) -> None:
        """``validate_payload(payload, barcode_format)``."""
        sig = inspect.signature(baobab_barcode.validate_payload)
        assert list(sig.parameters) == ["payload", "barcode_format"]

    def test_generate_signature_payload_and_keyword_only_options(self) -> None:
        """``generate`` : charge positionnelle, puis options en mots-clés uniquement."""
        sig = inspect.signature(baobab_barcode.generate)
        params = list(sig.parameters.values())
        assert params[0].name == "payload"
        assert params[0].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        assert params[1].name == "barcode_format"
        assert params[1].kind == inspect.Parameter.KEYWORD_ONLY
        for name in ("width", "height", "image_format", "include_text"):
            assert name in sig.parameters

    def test_decode_from_bytes_signature(self) -> None:
        """``decode_from_bytes`` : contenu positionnel, format attendu en mot-clé."""
        sig = inspect.signature(baobab_barcode.decode_from_bytes)
        params = list(sig.parameters.values())
        assert params[0].name == "content"
        assert "expected_format" in sig.parameters
        assert "strict_mode" in sig.parameters

    def test_decode_from_file_first_parameter_is_path(self) -> None:
        """``decode_from_file`` : premier paramètre ``path`` (Path ou str, voir doc)."""
        sig = inspect.signature(baobab_barcode.decode_from_file)
        assert list(sig.parameters)[:1] == ["path"]
        ann = sig.parameters["path"].annotation
        if isinstance(ann, str):
            assert "Path" in ann and "str" in ann
        else:
            assert ann == Path | str
