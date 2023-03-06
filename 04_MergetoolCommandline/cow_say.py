import cmd


class CowSay(cmd.Cmd):
    intro = "Moo!"

    def do_exit(self, arg):
        "CowSay End"
        return 1


if __name__ == "__main__":
    CowSay().cmdloop()
