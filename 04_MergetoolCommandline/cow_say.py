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
        eyes = int(args.pop(0))
    if args:
        tongue = bool(args.pop(0))
    return message, cow, eyes, tongue


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
        message, cow, eyes, tongue = cowsay_parse(arg)
        print(cowsay.cowsay(message=message, cow=cow, eyes=eyes, tongue=tongue))

    def do_cowthink(self, arg):
        message, cow, eyes, tongue = cowsay_parse(arg)
        print(cowsay.cowthink(message=message, cow=cow, eyes=eyes, tongue=tongue))


if __name__ == "__main__":
    CowSay().cmdloop()
