import cmd
import shlex
from cowsay import cowsay, list_cows, read_dot_cow, make_bubble


class CowSay(cmd.Cmd):
    intro = "Moo!"

    def do_exit(self, arg):
        """CowSay End"""
        return 1

    def do_list_cows(self, arg):
        """Lists all cow file names in the given directory"""
        if not arg:
            print(*list_cows())
        else:
            print(*list_cows(shlex.split(arg)[0]))

    def do_make_bubble(self, arg):
        """
            Wraps text if wrap_text is true, then pads text and sets inside a bubble.
            This is the text that appears above the cows
        """
        print(make_bubble(shlex.split(arg)[0]))


if __name__ == "__main__":
    CowSay().cmdloop()
