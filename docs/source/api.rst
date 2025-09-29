Plugins API
===========

.. currentmodule:: sphinx_syntax

If you wish to support a new parser generator, you'll need to implement
`ModelProvider` and call `register_provider` in your extension's ``setup`` function.

.. dropdown:: Extension template

    .. code-block:: python

        import pathlib

        import sphinx.application
        import sphinx.util.logging

        import sphinx_syntax

        _logger = sphinx.util.logging.getLogger(__name__)


        class MyProvider(sphinx_syntax.ModelProvider):
            # List all file extension your provider can parse.
            supported_extensions = {".yy", ".ll"}

            def __init__(self):
                self._cache: dict[pathlib.Path, sphinx_syntax.Model] = {}

            def from_file(self, path: pathlib.Path) -> sphinx_syntax.Model:
                # Normalize path.
                path = path.expanduser().resolve()

                if cached := self._cache.get(path):
                    return cached

                # Grammar name is equal to file name without suffix.
                name = path.stem

                # Check if file exists, report and return empty model if it doesn't.
                if not (path.exists() and path.is_file()):
                    _logger.error("unable to load %s: file not found", path)
                    model = self._cache[path] = sphinx_syntax.ModelImpl.empty(self, path, name)
                    return model

                # Process file and assemble a real model.
                model = self._cache[path] = sphinx_syntax.ModelImpl(self, path, name, ...)
                return model


        def setup(app: sphinx.application.Sphinx):
            app.setup_extension("sphinx_syntax")

            sphinx_syntax.register_provider(MyProvider())

            return {
                "version": "1.0.0",
                "parallel_read_safe": True,
                "parallel_write_safe": True,
            }


Basic interfaces
----------------

.. autofunction:: register_provider

.. autoclass:: ModelProvider
    :members:

.. autoclass:: Model
    :members:

.. autoclass:: ModelImpl

.. autoclass:: LoadingOptions
    :members:


Production rule descriptions
----------------------------

.. autoclass:: RuleBase
    :members:

.. autoclass:: ParserRule
    :members:

.. autoclass:: LexerRule
    :members:

.. autoclass:: Position
    :members:

.. autoclass:: Section
    :members:


Rule AST
--------

.. autoclass:: RuleContent
    :members:

.. autoclass:: Reference
    :members:

.. autoclass:: Doc
    :members:

.. autoclass:: Wildcard
    :members:

.. autodata:: WILDCARD

.. autoclass:: Negation
    :members:

.. autoclass:: ZeroPlus
    :members:

.. autoclass:: OnePlus
    :members:

.. autoclass:: Sequence
    :members:

.. autodata:: EMPTY

.. autoclass:: Alternative
    :members:

.. autoclass:: Literal
    :members:

.. autoclass:: Range
    :members:

.. autoclass:: CharSet
    :members:


AST visitors
------------

.. autoclass:: RuleContentVisitor
    :members:
    :undoc-members:

.. autoclass:: CachedRuleContentVisitor
    :members:
    :undoc-members:
