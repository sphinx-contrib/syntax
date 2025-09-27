# Code from https://github.com/pygments/pygments/pull/2913/
"""
pygments.lexers.yacc
~~~~~~~~~~~~~~~~~~~~

Lexers for Yacc grammars.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups, default, include, words
from pygments.lexers.c_cpp import CFamilyLexer  # type: ignore
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    Other,
    Punctuation,
    String,
    Whitespace,
)


class YaccLexer(RegexLexer):
    """
    Base for a Yacc lexer; needs language-specific tokens['ctypes'] specified.

    This is like an abstract base, and should not be used directly.  A language
    `foo' gets a YaccForFoo derived from YaccBase which highlights Yacc syntax
    and delegates the embedded language to Other (while not stopping on a '}'
    that appears in foo's strings or comments), a FooDelegate derived from
    FooLexer that also highlights Yacc-relevant keywords (if necessary), and a
    YaccFooLexer derived from DelegatingLexer which links the two and is exposed.
    """

    yaccName = r"[A-Za-z_][-\w.]*"
    sComment = r"//.*"
    mComment = r"(?s)/\*.*?\*/"
    _hexpart = r"[0-9a-fA-F](\'?[0-9a-fA-F])*"
    _decpart = r"\d(\'?\d)*"
    _ident = r"(?!\d)(?:[\w$]|\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})+"
    _intsuffix = r"(([uU][lL]{0,2})|[lL]{1,2}[uU]?)?"

    # fmt: off
    tokens = {
        # 'string' is a dependency of 'literals' and shouldn't be used directly
        "string": CFamilyLexer.tokens["string"],
        "literals": [
            (r'([LuU]|u8)?(")', bygroups(String.Affix, String), 'string'),
            (r"([LuU]|u8)?(')(\\.|\\[0-7]{1,3}|\\x[a-fA-F0-9]{1,2}|[^\\\'\n])(')",
             bygroups(String.Affix, String.Char, String.Char, String.Char)),

             # Hexadecimal floating-point literals (C11, C++17)
            (r'0[xX](' + _hexpart + r'\.' + _hexpart + r'|\.' + _hexpart +
             r'|' + _hexpart + r')[pP][+-]?' + _hexpart + r'[lL]?', Number.Float),

            (r'(-)?(' + _decpart + r'\.' + _decpart + r'|\.' + _decpart + r'|' +
             _decpart + r')[eE][+-]?' + _decpart + r'[fFlL]?', Number.Float),
            (r'(-)?((' + _decpart + r'\.(' + _decpart + r')?|\.' +
             _decpart + r')[fFlL]?)|(' + _decpart + r'[fFlL])', Number.Float),
            (r'(-)?0[xX]' + _hexpart + _intsuffix, Number.Hex),
            (r'(-)?0[bB][01](\'?[01])*' + _intsuffix, Number.Bin),
            (r'(-)?0(\'?[0-7])+' + _intsuffix, Number.Oct),
            (r'(-)?' + _decpart + _intsuffix, Number.Integer),
            (r'(true|false|NULL)\b', Name.Builtin),
            (_ident, Name)
        ],
        "yaccVarname": [
            (r"\$|-?\d+|[A-Za-z_]\w*|\[" + yaccName + r"\]", Name.Variable, "#pop"),
            default("#pop"),  # don't let a bad variable spoil the whole scan
        ],
        "yaccType": [
            (r"[*()]+", Punctuation),  # parentheses are for function pointers
            (r">", Punctuation, "#pop"),
            (r"\s+", Whitespace),
            (r"[A-Za-z]\w*", Name.Class),
        ],
        "yaccVars": [
            (
                r"(\$)(<)",
                bygroups(Name.Variable, Punctuation),
                ("yaccVarname", "yaccType"),
            ),
            (r"[@$]", Name.Variable, "yaccVarname"),
        ],
        # Mostly lifted from CFamilyLexer, but with Other instead of String,
        # because a string may actually be a Comment.PreprocFile
        "cstring": [
            (r'"', Other, "#pop"),
            (
                r"\\(.|x[a-fA-F0-9]{2,4}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|"
                + r"[0-7]{1,3})",
                Other,
            ),
            (r'[^\\"\n]+', Other),  # all other characters
            (r"\\\n", Other),  # line continuation
            (r"\\", Other),  # stray backslash
        ],
        "cBase": [
            (mComment, Other),
            (sComment, Other),
            include("yaccVars"),
            # Also pilfered from CFamilyLexer
            (r'([LuU]|u8)?"', Other, "cstring"),
            (
                r"([LuU]|u8)?(')(\\.|\\[0-7]{1,3}|\\x[a-fA-F0-9]{1,2}|[^\\\'\n])(')",
                Other,
            ),
        ],
        "embeddedC": [
            (r"\{", Other, "#push"),
            (r"\}", Other, "#pop"),
            include("cBase"),
            (r'[^{}$@/\'"]+|/', Other),
        ],
        "POSIXembeddedC": [
            (r"%\}", Punctuation, "#pop"),
            include("cBase"),
            (r'[^}$@%/\'"]+|[%}/]', Other),
        ],
        "common": [
            (r"\{", Other, "embeddedC"),
            (r"<", Punctuation, "yaccType"),
            (r"\s+", Whitespace),
            (mComment, Comment.Multiline),
            (sComment, Comment.Single),
            include("yaccVars"),
            include("literals"),
        ],
        "gettext": [
            # GNU Bison specially allows gettext calls around string tokens
            # (which are also a Bison extension)
            (r"\)", Punctuation, "#pop"),
            include("common"),
        ],
        "define": [
            (
                r"(api\.value\.type)(\s+)(union(?:-directive)?|variant)\b",
                bygroups(Name, Whitespace, Keyword),
                "#pop",
            ),
            (
                r"(api\.value\.union\.name)(\s+)([A-Za-z_]\w*)\b",
                bygroups(Name, Whitespace, Name.Class),
                "#pop",
            ),
            (
                r"(api\.(?:header|location)\.include)(\s+)"
                + r'(\{)(\s*)("[^"]+"|<[^>]+>)(\s*)(\})',
                bygroups(
                    Name,
                    Whitespace,
                    Punctuation,
                    Whitespace,
                    Comment.PreprocFile,
                    Whitespace,
                    Punctuation,
                ),
                "#pop",
            ),
            default("#pop"),
        ],
        "declarations": [
            # According to POSIX, just a `%%' token is enough; it doesn't
            # necessarily have to be on its own line
            (r"%%", Keyword, "#pop"),
            (r"%\{", Punctuation, "POSIXembeddedC"),
            (
                r"^(%)(define)(\s+)",
                bygroups(Punctuation, Keyword, Whitespace),
                "define",
            ),
            (r"^(%)([\w-]+)", bygroups(Punctuation, Keyword)),
            (r";", Punctuation),
            (r"(_)(\()", bygroups(Name.Function.Magic, Punctuation), "gettext"),
            (yaccName, Name),
            include("common"),
        ],
        "predicate": [
            # Hackily support GNU Bison GLR predicates.  This just keeps
            # the braces balanced
            (r"\{", Other, "embeddedC"),
            include("common"),
        ],
        "rules": [
            (r"%%", Keyword, "#pop"),
            (r"%\?", Keyword, "predicate"),
            (r"[:;|]", Operator),
            (words(("empty", "prec"), prefix="%", suffix=r"\b"), Keyword),
            (r"\berror\b", Keyword),
            (
                r"(" + yaccName + r")(?:(\[)(" + yaccName + r")(\]))?",
                bygroups(Name, Punctuation, Name, Punctuation),
            ),
            (
                yaccName + r"(?:(\[)" + yaccName + r"(\]))?",
                bygroups(Name, Punctuation, Name, Punctuation),
            ),
            include("common"),
        ],
        "root": [  # aka Yacc `epilogue'
            # Just defer everything to the C lexer
            (r"(?s).+", Other)
        ],
    }
    # fmt: on

    # Set a default stack
    def get_tokens_unprocessed(self, text, stack=("root", "rules", "declarations")):
        yield from RegexLexer.get_tokens_unprocessed(self, text, stack)
