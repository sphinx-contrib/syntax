import pathlib
import re
import shutil
import subprocess

DIR = pathlib.Path(__file__).parent

TYPE_REPLACE_TOKEN = re.compile(
    r"^(\s*self\.[a-zA-Z0-9_]+ = None) # Token$", re.MULTILINE
)
TYPE_REPLACE_TOKEN_LIST = re.compile(
    r"^(\s*self\.[a-zA-Z0-9_]+ = list\(\)) # of Tokens$", re.MULTILINE
)
TYPE_REPLACE = re.compile(
    r"^(\s*self\.[a-zA-Z0-9_]+ = None) # ([a-zA-Z0-9_]+)$", re.MULTILINE
)
TYPE_REPLACE_LIST = re.compile(
    r"^(\s*self\.[a-zA-Z0-9_]+ = list\(\)) # of ([a-zA-Z0-9_]+)s$", re.MULTILINE
)


def main():
    shutil.rmtree(DIR / "gen", ignore_errors=True)
    DIR.joinpath("gen").mkdir(parents=True, exist_ok=True)
    DIR.joinpath("gen/__init__.py").touch()
    shutil.copyfile(DIR / "ANTLRv4LexerBase.py.in", DIR / "gen/ANTLRv4LexerBase.py")
    shutil.copyfile(DIR / "BisonLexerBase.py.in", DIR / "gen/BisonLexerBase.py")
    subprocess.check_call(
        [
            "antlr4",
            "-Dlanguage=Python3",
            "-visitor",
            "-listener",
            "ANTLRv4Parser.g4",
            "ANTLRv4Lexer.g4",
            "-o",
            "gen",
        ],
        cwd=DIR,
    )
    subprocess.check_call(
        [
            "antlr4",
            "-Dlanguage=Python3",
            "-visitor",
            "-listener",
            "BisonParser.g4",
            "BisonLexer.g4",
            "-o",
            "gen",
        ],
        cwd=DIR,
    )

    for name in ["ANTLRv4Parser", "BisonParser"]:
        path = DIR.joinpath(f"gen/{name}.py")
        parser_text = path.read_text()
        parser_text = TYPE_REPLACE_TOKEN.sub(r"\1 # type: Token", parser_text)
        parser_text = TYPE_REPLACE_TOKEN_LIST.sub(
            r"\1 # type: list[Token]", parser_text
        )
        parser_text = TYPE_REPLACE.sub(r"\1 # type: %s.\2" % name, parser_text)
        parser_text = TYPE_REPLACE_LIST.sub(
            r"\1 # type: list[%s.\2]" % name, parser_text
        )
        path.write_text(parser_text)


if __name__ == "__main__":
    main()
