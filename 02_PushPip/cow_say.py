import argparse
from cowsay import cowsay, list_cows, read_dot_cow


def parse_options():
    parser = argparse.ArgumentParser()

    mapper = {
        "e": "eyes",
        "f": "cowfile",
        "T": "tongue",
        "W": "width",
        "l": "list",
        "n": "wrap_text",
    }

    parser.add_argument("-e", type=str)
    parser.add_argument("-f")
    parser.add_argument("-T")
    parser.add_argument("-W")
    parser.add_argument("-l", action='store_true')
    parser.add_argument("-n", action='store_false')

    parser.add_argument("-b", action='store_true')
    parser.add_argument("-d", action='store_true')
    parser.add_argument("-g", action='store_true')
    parser.add_argument("-p", action='store_true')
    parser.add_argument("-s", action='store_true')
    parser.add_argument("-t", action='store_true')
    parser.add_argument("-w", action='store_true')
    parser.add_argument("-y", action='store_true')

    args, unparsed = parser.parse_known_args()
    message = " ".join(unparsed)

    arguments = dict()
    arguments["message"] = message

    PRESETS = "bggpstwy"
    preset = None
    for p in PRESETS:
        if getattr(args, p):
            preset = p
            break
    arguments["preset"] = preset

    for key in mapper:
        if getattr(args, key):
            arguments[mapper[key]] = getattr(args, key)

    return arguments


def main():
    arguments = parse_options()
    if "list" in arguments:
        print(*list_cows())
    else:
        if "cowfile" in arguments and '/' in arguments["cowfile"]:
            with open(arguments["cowfile"]) as file:
                arguments["cowfile"] = read_dot_cow(file)

        print(cowsay(**arguments))


if __name__ == "__main__":
    main()
