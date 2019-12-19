#!/usr/bin/env python3
from threading import Thread, Lock
from random import choice, randint
from time import sleep

from progbar import TextProgressBar

running_threads = []
console_lock = Lock()

tests = [
    (TextProgressBar('17.0.133.54', 100, 0, 5000, console_lock=console_lock, show_percent=True), 4),
    (TextProgressBar('103.49.13.254', 100, 0, 5000, console_lock=console_lock, show_percent=True), 5),
    (TextProgressBar('217.10.1.4', 100, 0, 5000, console_lock=console_lock, show_percent=True), 6),
    (TextProgressBar('112.190.33.154', 100, 0, 5000, console_lock=console_lock, show_percent=True), 7),
]


def update(progbar, line):
    while not progbar.complete:
        sleep(randint(1, 3))
        progbar.add(randint(150, 450))
        progbar.render(linenum=line)


def main():
    for test in tests:
        # Pre-render
        test[0].render(linenum=test[1])
        thread = Thread(target=update, args=test, name=test[0])
        running_threads.append(thread)
        thread.start()

    for thread in running_threads:
        thread.join()

    print

if __name__ == '__main__':
    main()
