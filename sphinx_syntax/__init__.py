import pathlib

import sphinx.application
import sphinx.builders.html
from syntax_diagrams import SvgRenderSettings, TextRenderSettings
from sphinx.util.fileutil import copy_asset_file as _copy_asset_file

import sphinx_syntax.diagram
import sphinx_syntax.domain
from sphinx_syntax._version import *
from sphinx_syntax.api import (
    AutodocProvider,
    Grammar,
    Object,
    Rule,
    register_provider,
)

# Public API
__all__ = [
    "register_provider",
    "AutodocProvider",
    "Grammar",
    "Object",
    "Rule",
    "SvgRenderSettings",
    "TextRenderSettings",
]


def _copy_asset_files(app: sphinx.application.Sphinx, exc: Exception | None):
    if isinstance(app.builder, sphinx.builders.html.StandaloneHTMLBuilder) and not exc:
        custom_file = pathlib.Path(__file__).parent / "static/railroad-diagrams.css"
        static_dir = app.outdir / "_static"
        _copy_asset_file(custom_file, static_dir)


def setup(app: sphinx.application.Sphinx):
    app.add_domain(sphinx_syntax.domain.SyntaxDomain)
    app.add_directive_to_domain(
        "syntax", "diagram", sphinx_syntax.diagram.DiagramDirective
    )
    app.add_post_transform(sphinx_syntax.diagram.ProcessDiagrams)
    app.add_config_value(
        "railroad_diagrams_text_settings",
        TextRenderSettings(),
        "html",
        TextRenderSettings,
    )
    app.add_config_value(
        "railroad_diagrams_svg_settings",
        SvgRenderSettings(),
        "html",
        SvgRenderSettings,
    )
    app.connect("build-finished", _copy_asset_files)
    app.add_css_file("railroad-diagrams.css")

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
