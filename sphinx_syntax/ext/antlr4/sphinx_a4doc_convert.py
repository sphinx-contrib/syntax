import argparse
import difflib
import glob
import pathlib
import re
import sys

from sphinx.util.console import colorize


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        help="path to an RST file or a glob",
        nargs="*",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="actually run replacements",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="print the full diff at the end of a dry run",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print verbose statistics",
    )

    ns = parser.parse_args()

    fulldiff: list[str] = []

    if not ns.path:
        ns.path = [str(pathlib.Path.cwd())]

    if ns.run:
        run_type = "Run"
    else:
        run_type = "Dry-run"
    if len(ns.path) == 1:
        print(colorize("bold", f"{run_type} for {ns.path[0]}"), file=sys.stderr)
    else:
        print(
            colorize("bold", f"{run_type} for {len(ns.path)} paths/globs"),
            file=sys.stderr,
        )

    paths = [
        pathlib.Path(filename)
        for path in ns.path
        for dest in glob.glob(path, recursive=True)
        for filename in (
            glob.glob(dest + "/**", recursive=True)
            if pathlib.Path(dest).is_dir()
            else [dest]
        )
    ]
    paths.sort()

    if not paths:
        print(
            colorize("yellow", "No files found"),
            file=sys.stderr,
        )
        return

    max_len = (
        max(
            len(str(path))
            for path in paths
            if ns.verbose or path.suffix in [".rst", ".g4"]
        )
        + 1
    )

    for path in paths:
        if path.suffix == ".rst":
            text = orig_text = path.read_text()

            text = re.sub(
                r"^([ ]*)\.\.[ ]+a4:autogrammar::[ ]*(.*?)(\.g4)?[ ]*$",
                r"\1.. syntax:autogrammar:: \2.g4",
                text,
                flags=re.MULTILINE,
            )
            text = re.sub(
                r"^([ ]*)\.\.[ ]+a4:autorule::[ ]*(\S*?)(\.g4)?[ ]",
                r"\1.. syntax:autorule:: \2.g4 ",
                text,
                flags=re.MULTILINE,
            )
            text = re.sub(
                r"^([ ]*)\.\.[ ]+a4:(autogrammar|grammar|autorule|rule)::",
                r"\1.. syntax:\2::",
                text,
                flags=re.MULTILINE,
            )
            text = re.sub(
                r"^([ ]*)\.\.[ ]+railroad-diagram::",
                r"\1.. syntax:diagram::",
                text,
                flags=re.MULTILINE,
            )
            text = re.sub(
                r"^([ ]*)\.\.[ ]+lexer-rule-diagram::",
                r"\1.. syntax:lexer-diagram::",
                text,
                flags=re.MULTILINE,
            )
            text = re.sub(
                r"^([ ]*)\.\.[ ]+parser-rule-diagram::",
                r"\1.. syntax:parser-diagram::",
                text,
                flags=re.MULTILINE,
            )
            text = re.sub(
                r"\n[ ]+:type:[ ]+(mixed|lexer|parser)[ ]*",
                "",
                text,
                flags=re.MULTILINE,
            )
            text = re.sub(
                r"^([ ]+):only-reachable-from:",
                r"\1:root-rule:",
                text,
                flags=re.MULTILINE,
            )
            text = re.sub(
                r":a4:(g|r|grammar|rule):`",
                r":syntax:\1:`",
                text,
                flags=re.MULTILINE,
            )
        elif path.suffix == ".g4":
            text = orig_text = path.read_text()

            text = re.sub(
                r"^([ ]*//@[ ]*)doc:nodoc[ ]*$",
                r"\1doc:no-doc",
                text,
                flags=re.MULTILINE,
            )
        else:
            if ns.verbose:
                print(
                    colorize("faint", f"  {str(path):<{max_len}} | skip"),
                    file=sys.stderr,
                )
            continue

        if text == orig_text:
            print(
                colorize("faint", f"  {str(path):<{max_len}} | unchanged"),
                file=sys.stderr,
            )
            continue

        diff = list(
            difflib.unified_diff(
                orig_text.splitlines(keepends=True),
                text.splitlines(keepends=True),
                fromfile=str(path),
                tofile=str(path),
            )
        )

        additions = 0
        deletions = 0
        for line in diff:
            if line.startswith("+") and not line.startswith("+++"):
                additions += 1
            elif line.startswith("-") and not line.startswith("---"):
                deletions += 1

        print(
            f"  {str(path):<{max_len}} | +{colorize("green", str(additions))} -{colorize("red", str(deletions))}",
            file=sys.stderr,
        )
        fulldiff += diff

        for directive in ["docstring-marker", "members-marker"]:
            if f".. {directive}::" in text:
                print(
                    colorize(
                        "yellow",
                        f"    Warning: directive 'a4:{directive}' is not available anymore",
                    ),
                    file=sys.stderr,
                )

        if ns.run:
            path.write_text(text)

    if not fulldiff:
        print("", file=sys.stderr)
        print(colorize("bold", f"No changes detected"), file=sys.stderr)
    elif ns.diff:
        print("", file=sys.stderr)
        print(colorize("bold", f"Diff:"), file=sys.stderr)

        def cl(line: str):
            if (
                line.startswith("---")
                or line.startswith("+++")
                or line.startswith("@@")
            ):
                return colorize("bold", colorize("fuchsia", line))
            elif line.startswith("+"):
                return colorize("green", line)
            elif line.startswith("-"):
                return colorize("red", line)
            else:
                return line

        print("".join(map(cl, fulldiff)), end="")

    if not ns.run and fulldiff:
        print("", file=sys.stderr)
        if not ns.diff:
            print(
                colorize(
                    "bold",
                    f"Restart with flag --diff to see changes, --run to apply them",
                ),
                file=sys.stderr,
            )
        else:
            print(
                colorize("bold", f"Restart with flag --run to apply changes"),
                file=sys.stderr,
            )


if __name__ == "__main__":
    main()
