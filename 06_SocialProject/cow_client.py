import select
import sys
import cmd
import shlex
import socket
import readline
import threading

locker = threading.Lock()


class CowClient(cmd.Cmd):
    def do_who(self, args):
        send("who\n")

    def do_login(self, args):
        send(f"login {shlex.split(args)[0]}\n")

    def complete_login(self, text, line, beg, end):
        with locker:
            send(f"cows\n")
            msg = receive(timeout=None)
            for c in ["'", "[", "]", ","]:
                msg = msg.replace(c, "")
            cows = msg.strip().split()[2:]
            return [s for s in cows if s.startswith(text)]

    def do_cows(self, args):
        send("cows\n")

    def do_exit(self, args):
        send("exit\n")
        return 1

    def do_yield(self, args):
        send(f"yield {args.strip()}\n")

    def do_say(self, args):
        send(f"say {args.strip()}\n")

    def complete_say(self, text, line, beg, end):
        with locker:
            if len(text.split()) <= 1:
                send("who\n")
                msg = receive(timeout=None)
                for c in ["'", "[", "]", ","]:
                    msg = msg.replace(c, "")
                who = msg.strip().split()[2:]
                return [s for s in who if s.startswith(text)]


def send(msg):
    s.send(msg.encode())


def receive(timeout):
    readable, _, _ = select.select([s], [], [], timeout)
    for soc in readable:
        msg = soc.recv(1024).decode()
        return msg
    return None


def messenger(cmdline):
    while True:
        with locker:
            msg = receive(timeout=0.)
        if msg:
            print(msg.strip())
            print(f"{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1337))
    s.setblocking(False)
    cmdline = CowClient()
    gm = threading.Thread(target=messenger, args=(cmdline,))
    gm.start()
    cmdline.cmdloop()
