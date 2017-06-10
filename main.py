from queue import Queue
import random as r
import sys
import threading
import time


class Initiation():
    def __init__(self):
        self.q = Queue()
        self.game_end = 0
        self.points = 0
        self.duration = 0
        self.time_left = 10
        self.print_lock = threading.Lock()
        self.time_left_lock = threading.Lock()


def timer():
    time.sleep(1)
    with I.time_left_lock:
        I.time_left -= 1
    I.duration += 1
    if I.time_left == 0:
        message("\nTime's up!")
        I.game_end = 1


def game():
    x = r.randint(0,10)
    y = r.randint(0,10)
    ss = '{} + {} = '.format(x,y)
    while 1:
        try:
            answer = int(input(ss))
            if check_answer(answer,x,y) == 1 or I.time_left == 0:
                break
        except ValueError:
            if I.time_left == 0:
                break
            message('Only numbers!')
        except (KeyboardInterrupt, EOFError):
            message('\nAbort!')
            I.game_end = 1
            break


def check_answer(answer,x,y):
    if answer == (x + y):
        correct = 'Correct! Time left: {} sec.'.format(I.time_left)
        message(correct,1)
        I.points += 1
        return 1
    wrong = 'Wrong! Time left: {} sec.'.format(I.time_left)
    message(wrong)
    return 0


def message(msg,type=0):
    if type == 0:                                            # red
        with I.print_lock:
            print('\x1b[0;31;40m' + msg + '\x1b[0m')
    else:                                                   # green
        with I.print_lock:
            print('\x1b[0;32;40m' + msg + '\x1b[0m')


def threader_timer():
    while I.time_left != 0 and I.game_end != 1:
        timer()
    I.q.task_done()


def threader_game():
    while I.game_end != 1:
        game()
    I.q.task_done()


def main():
    t = threading.Thread(target=threader_timer)
    g = threading.Thread(target=threader_game)
    t.daemon = True
    g.daemon = True
    t.start()
    g.start()
    for worker in range(2):
        I.q.put(worker)
    try:
        I.q.join()
    except KeyboardInterrupt:
        ...
    msg = ' === Game Over ===\nPoints: {}\nDuration: {}'.format(I.points, I.duration)
    message(msg,1)


if __name__ == '__main__':
    I = Initiation()
    main()
else:
    I = Initiation()
