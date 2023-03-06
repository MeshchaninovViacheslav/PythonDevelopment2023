import cmd
import shlex
import cowsay


def cowsay_parse(arg):
    cow = 'default'
    eyes = cowsay.Option.eyes
    tongue = cowsay.Option.tongue

    args = shlex.split(arg)
    message = args.pop(0)
    if args:
        cow = args.pop(0)
    if args:
        eyes = args.pop(0)
    if args:
        tongue = args.pop(0)
    return message, cow, eyes, tongue


def complete(text, line, beg, end):
    args = shlex.split(line)
    idx = len(args) - 2
    if beg == end:
        idx += 1

    data = {
        "cows": cowsay.list_cows(),
        "eyes": ["OO", "$$", "XX", "@@", "##"],
        "tongues": ["U ", "UU", "MM", "WW", "VV"]
    }

    key = ["cows", "eyes", "tongues"][idx - 1]
    return [c for c in data[key] if c.startswith(text)]


class CowSay(cmd.Cmd):
    intro = "Moo!"

    def do_exit(self, arg):
        """CowSay End"""
        return 1

    def do_list_cows(self, arg):
        """Lists all cow file names in the given directory"""
        if not arg:
            print(*cowsay.list_cows())
        else:
            print(*cowsay.list_cows(shlex.split(arg)[0]))

    def do_make_bubble(self, arg):
        """
            Wraps text if wrap_text is true, then pads text and sets inside a bubble.
            This is the text that appears above the cows
        """
        brackets = cowsay.THOUGHT_OPTIONS['cowsay']
        width = 40
        wrap_text = True

        args = shlex.split(arg)
        text = args.pop(0)
        if args:
            brackets = args.pop(0)
        if args:
            width = int(args.pop(0))
        if args:
            wrap_text = bool(args.pop(0))

        print(cowsay.make_bubble(text, brackets, width, wrap_text))

    def do_cowsay(self, arg):
        """Returns the resulting cowsay string"""
        message, cow, eyes, tongue = cowsay_parse(arg)
        print(cowsay.cowsay(message=message, cow=cow, eyes=eyes, tongue=tongue))

    def do_cowthink(self, arg):
        """Returns the resulting cowthink string"""
        message, cow, eyes, tongue = cowsay_parse(arg)
        print(cowsay.cowthink(message=message, cow=cow, eyes=eyes, tongue=tongue))

    def complete_cowsay(self, text, line, beg, end):
        """Autocomplete for cowsay"""
        return complete(text, line, beg, end)

    def complete_cowthink(self, text, line, beg, end):
        """Autocomplete for cowsay"""
        return complete(text, line, beg, end)

    def complete_make_bubble(self, text, line, beg, end):
        args = shlex.split(line)
        idx = len(args) - 2
        if beg == end:
            idx += 1

        if idx == 3:
            return [c for c in ['True', 'False'] if c.lower().startswith(text.lower())]


if __name__ == "__main__":
    CowSay().cmdloop()
