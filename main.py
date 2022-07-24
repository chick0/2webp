from os import name
from os import mkdir
from os import listdir
from os import remove
from os.path import join
from os.path import exists
from os.path import dirname
from sys import argv
from sys import exit
from typing import NamedTuple
from subprocess import run

INPUT = join(".", "input")
OUTPUT = join(".", "output")


class PathData(NamedTuple):
    input: str
    output: str
    x: str


def test_path():
    if not exists(INPUT):
        mkdir(INPUT)

    if not exists(OUTPUT):
        mkdir(OUTPUT)
    else:
        for target_to_delete in listdir(OUTPUT):
            remove(path=join(OUTPUT, target_to_delete))


def test_libwebp():
    if name == "nt":
        try:
            output = run("cwebp.exe -version", capture_output=True, check=False)
        except FileNotFoundError:
            print(f"Can't find 'cwebp.exe' in {dirname(__file__)!r}")
            print("Download libwebp from 'https://storage.googleapis.com/downloads.webmproject.org/releases/webp/index.html'")
            exit(-1)

        version = output.stdout.decode().strip()
        print(f"* libwepb version : {version}")
    else:
        raise NotImplementedError


def get_ouput(name: str) -> str:
    name = name.rsplit(".", 1)[0]
    return name + ".webp"


def get_images() -> list[PathData]:
    return [
        PathData(
            input=join(INPUT, x),
            output=join(OUTPUT, get_ouput(name=x)),
            x=x
        ) for x in listdir(INPUT)
        if x.endswith(".png") or x.endswith(".jpg") or "--ignore-ext" in argv
    ]


def get_quailty() -> int:
    try:
        index = argv.index("-q")
        quailty = int(argv[index + 1])

        if quailty < 0 or quailty > 100:
            raise ValueError
    except (ValueError, IndexError):
        quailty = 75
    finally:
        return quailty


def get_command(path: PathData) -> str:
    exec = "cwebp"

    if name == "nt":
        exec += ".exe"

    return exec + f" -q {get_quailty()} {path.input} -o {path.output}"


def main():
    targets = get_images()
    for target in targets:
        print("*", target.x)
        run(
            get_command(
                path=target
            ),
            check=False
        )

        print("\n")


if __name__ == "__main__":
    test_path()
    test_libwebp()
    print("* set quailty to", get_quailty(), end="\n\n")
    main()
