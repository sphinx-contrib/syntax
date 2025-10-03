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
        "src/diagram-resolver-data.html",
        "src/diagram-override.html",
        "src/diagram-opt.html",
        "src/objects.html",
        "src/refs.html",
        "src/audodoc-lexer.html",
        "src/audodoc-bison.html",
        "src/audodoc-rule.html",
        "src/root-rule.html",
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
def test_warnings(app):
    app.build()
    warnings = app.warning.getvalue()
    assert "syntax:rule can't be used outside of a diagram" in warnings
    assert (
        "trying to document rule input as part of grammar WrongGrammar, "
        "but the rule is defined in grammar Bison" in warnings
    )
    assert "'syntax:diagram' directive doesn't support option :name:" in warnings
    assert "diagram descriptions can't have custom resolver_data" in warnings
    assert "can't parse syntax diagram description" in warnings
    assert "invalid-yaml.rst" in warnings
    assert "line 9," in warnings
    assert "this yaml is invalid!" in warnings
