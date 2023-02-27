import argparse
import os
import io
import random
from urllib.request import urlopen
from cowsay import cowsay, list_cows, read_dot_cow


def bullscows(guess: str, secret: str) -> (int, int):
    if len(guess) != len(secret):
        raise ValueError("Длины guess и secret должны совпадать")
    bull_n = 0
    cow_n = 0
    for i, c in enumerate(guess):
        if c in secret:
            if secret[i] == c:
                bull_n += 1
            else:
                cow_n += 1
    return bull_n, cow_n


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    if not words:
        return 0
    secret = random.choice(words)
    tries = 0

    while True:
        guess = ask("Введите слово: ", words)
        tries += 1
        bull_n, cow_n = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", bull_n, cow_n)
        if bull_n == len(secret):
            break

    return tries


def ask(prompt: str, valid: list[str] = None) -> str:
    COW = read_dot_cow(io.StringIO("""
    $the_cow = <<EOC;
       $thoughts
        $thoughts
         $thoughts
                    '-.
          .---._     \\ \.--'
        /       `-..__)  ,-'
       |    0           /
        \--.__,   .__.,`
         `-.___'._\\_.'
    
    EOC"""))
    while True:
        print(cowsay(prompt, cowfile=COW))
        guess = input()
        if valid and guess not in valid:
            print(cowsay("Слова нет в словаре.", cowfile=COW))
        else:
            break
    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(cowsay(format_string.format(bulls, cows), random.choice(list_cows())))


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("dictionary", help="Path or url")
    parser.add_argument("length", nargs="?", help="Word length", default=5, type=int)
    return parser.parse_args()


def read_dict(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            dictionary = [x.strip() for x in f.readlines()]
    else:
        with urlopen(path) as f:
            dictionary = [x.decode("utf-8").strip() for x in f.readlines()]
    return dictionary


def main() -> None:
    args = parse_options()
    dictionary = read_dict(args.dictionary)
    if args.length:
        dictionary = [word for word in dictionary if len(word) == args.length]
    tries = gameplay(ask, inform, dictionary)
    print(f"Количество попыток: {tries}")


if __name__ == "__main__":
    main()
