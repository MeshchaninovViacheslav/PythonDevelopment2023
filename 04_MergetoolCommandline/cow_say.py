import cmd
import shlex
import cowsay


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

    # def do_cowthimaknk(self, arg):
    #     """Returns the resulting cowthink string"""
    #     print(cowthink(shlex.split(arg)[0]))


if __name__ == "__main__":
    CowSay().cmdloop()
