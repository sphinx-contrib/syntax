import datetime

import sphinx_syntax

project = "Sphinx Syntax"
copyright = f"{datetime.date.today().year}, Tamika Nomara"
author = "Tamika Nomara"
release = version = sphinx_syntax.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinxcontrib.cairosvgconverter",
    "sphinx_design",
    "sphinx_syntax",
]

templates_path = ["_templates"]
exclude_patterns = []

primary_domain = "py"
default_role = "py:obj"
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "syntax_diagrams": ("https://syntax-diagrams.readthedocs.io/en/stable/", None),
}
autodoc_member_order = "bysource"
nitpick_ignore_regex = [(r"py:class", r".*\.T")]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_extra_path = ["_extra/robots.txt"]
html_theme_options = {
    "source_repository": "https://github.com/sphinx-contribs/sphinx-syntax",
    "source_branch": "main",
    "source_directory": "docs/source",
}


def setup(app):
    import pathlib
    import sys

    sys.path.append(str(pathlib.Path(__file__).parent / "_extensions"))

    from yacc_hl import YaccLexer  # type: ignore

    app.add_lexer("bison", YaccLexer)
