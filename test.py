#!/usr/bin/env python3
from threading import Thread
from random import choice, randint
from time import sleep

from progbar import TextProgressBar

running_threads = []

tests = [
    (TextProgressBar('17.0.133.54', 100, 0, 5000), 4),
    (TextProgressBar('103.49.13.254', 100, 0, 5000), 5),
    (TextProgressBar('217.10.1.4', 100, 0, 5000), 6),
    (TextProgressBar('112.190.33.154', 100, 0, 5000), 7),
]


def update(progbar, line):
    while not progbar.complete:
        sleep(randint(1, 4))
        progbar.add(randint(50, 250))
        progbar.render(linenum=line)


def main():
    for test in tests:
        thread = Thread(target=update, args=test, name=test[0])
        running_threads.append(thread)
        thread.start()

    for thread in running_threads:
        thread.join()

if __name__ == '__main__':
    main()
