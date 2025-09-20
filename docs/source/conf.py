import datetime

import sphinx_syntax

project = "Sphinx Railroad Diagrams"
copyright = f"{datetime.date.today().year}, Tamika Nomara"
author = "Tamika Nomara"
release = version = sphinx_syntax.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.githubpages",
    "sphinx_design",
    "sphinx_syntax",
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_extra_path = ["_extra/robots.txt"]
html_theme_options = {
    "source_repository": "https://github.com/taminomara/sphinx-syntax",
    "source_branch": "main",
    "source_directory": "docs/source",
}
