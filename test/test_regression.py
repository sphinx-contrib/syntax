import pathlib

import pytest
from bs4 import BeautifulSoup


@pytest.mark.sphinx("html", testroot="doc")
@pytest.mark.test_params(shared_result="test_regression")
@pytest.mark.parametrize(
    "src",
    [
        "src/diagrams.html",
        "src/diagram-settings.html",
        "src/diagram-refs.html",
        "src/diagram-override.html",
        "src/diagram-opt.html",
        "src/objects.html",
        "src/refs.html",
        "src/audodoc-lexer.html",
        "src/audodoc-bison.html",
    ],
)
def test_regression(app, src, file_regression):
    app.build()
    path = pathlib.Path(app.outdir) / src
    soup = BeautifulSoup(path.read_text("utf8"), "html.parser")
    content = soup.select_one("div.regression")
    assert content
    file_regression.check(
        content.prettify(),
        basename="doc-" + pathlib.Path(src).stem,
        extension=".html",
        encoding="utf8",
    )


@pytest.mark.sphinx("html", testroot="doc")
@pytest.mark.test_params(shared_result="test_regression")
def test_invalid_yaml(app):
    app.build()
    warnings = app.warning.getvalue()
    assert "can't parse syntax diagram description" in warnings
    assert "invalid-yaml.rst" in warnings
    assert "line 9," in warnings
    assert "this yaml is invalid!" in warnings
