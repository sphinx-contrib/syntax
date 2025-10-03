# Changelog

## [unreleased]

## [1.1.1]

- Updated migration script to convert `autorule`.

## [1.1.0]

- Added `syntax:autorule`.

- Fixed bugs related to propagating options to nested objects.

- Autodoc-related options can be used with the `diagram` directive,
  they'll be picked up by nested `autorule`, `lexer-diagram`, and `parser-diagram`.

- Clarified documentation around the `:import:` option. It only has effect
  on grammar declarations, despite documentation mentioning that it can be used
  on diagrams.

- Fixed links after move.

- Releases are no longer uploaded to test version of PyPi.

## [1.0.1-post1]

- Migrated documentation to Read the Docs.

- Moved repository to [sphinx-contrib](https://github.com/sphinx-contrib) organization.

## [1.0.1]

- Fix parsing of inline code in Bison grammars.

- Fix spurious "duplicate description" warning in multithreaded builds.

## [1.0.0-post1]

- Fix readme title.

## [1.0.0]

- Initial release.

[unreleased]: https://github.com/sphinx-contrib/syntax/compare/v1.1.1...HEAD
[1.1.1]: https://github.com/sphinx-contrib/syntax/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/sphinx-contrib/syntax/compare/v1.0.1-post1...v1.1.0
[1.0.1-post1]: https://github.com/sphinx-contrib/syntax/compare/v1.0.1...v1.0.1-post1
[1.0.1]: https://github.com/sphinx-contrib/syntax/compare/v1.0.0-post1...v1.0.1
[1.0.0-post1]: https://github.com/sphinx-contrib/syntax/compare/v1.0.0...v1.0.0-post1
[1.0.0]: https://github.com/sphinx-contrib/syntax/releases/tag/v1.0.0
