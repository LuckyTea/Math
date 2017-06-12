from queue import Queue
import random as r
import sys
import threading
import time


class Initiation():
    def __init__(self):
        self.q = Queue()
        self.combo = 0
        self.combo_max = 0
        self.combo_limit = 20
        self.duration = 0
        self.game_end = 0
        self.points = 0
        self.time_left = 10
        self.lvl = 0
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
    ss = task()
    while 1:
        try:
            user = int(input(ss[0]))
            if check_answer(user,ss[1]) == 1 or I.time_left == 0:
                break
        except ValueError:
            if I.time_left == 0:
                break
            message('Only numbers!')
        except (KeyboardInterrupt, EOFError):
            message('\nAbort!')
            I.game_end = 1
            break


def task():
    o = ('+', '-', '*', '/')
    operation = {
        '+': (lambda x,y: x + y),
        '-': (lambda x,y: x - y),
        '*': (lambda x,y: y * y),
        '/': (lambda x,y: y / y)
    }
    if I.lvl in (0,1):
        max = {0:11, 1:51}[I.lvl]                           # a +|- b
        a = r.randrange(0,max)
        b = r.randrange(0,max)
        o1 = o[r.randrange(0,2)]
        text = '{a} {o1} {b} = '.format(a=a,b=b,o1=o1)
        answer = operation[o1](a,b)
        return (text,answer)
    elif I.lvl in (2,3,4):                                  # a +|- b +|- c
        max = {2:31, 3:61, 4:101}[I.lvl]
        a = r.randrange(0,max)
        b = r.randrange(0,max)
        c = r.randrange(0,max)
        o1 = o[r.randrange(0,2)]
        o2 = o[r.randrange(0,2)]
        text = '{a} {o1} {b} {o2} {c} = '.format(a=a,b=b,c=c,o1=o1,o2=o2)
        answer = operation[o2](operation[o1](x,y),c)
        return (text,answer)


def check_answer(user,answer):
    if user == answer:
        msg = 'Correct! Time left: {} sec. Combo: {}'.format(I.time_left, I.combo)
        message(msg,1)
        reward(1)
        return 1
    msg = 'Wrong! Time left: {} sec.'.format(I.time_left)
    message(msg)
    reward()
    return 0


def reward(type=0):
    if type == 0:
        I.combo = 0
    elif type == 1:
        if I.lvl in (0,1):
            point_plus = 1 if I.combo < 2 else I.combo
            time_plus = 1
        elif I.lvl in (2,3,4):
            point_plus = 5 if I.combo < 2 else 5 * I.combo
            time_plus = 2
        with I.time_left_lock:
            I.time_left += time_plus
        I.points += point_plus
        I.combo += 1 if I.combo < I.combo_limit else 0
        I.combo_max = I.combo if I.combo >= I.combo_max else I.combo_max
        if I.combo_max is 5:
            I.lvl = 1
        elif I.combo_max is 10:
            I.lvl = 2
        elif I.combo_max is 15:
            I.lvl = 3
        elif I.combo_max is 20:
            I.lvl = 4


def game_over():
    msg = '\n === Game Over ===\nPoints: {}\nMax Combo: {}\nDuration: {}'.format(I.points, I.combo_max, I.duration)
    message(msg,1)


def message(msg,type=0):
    if type == 0:                                           # red
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
    game_over()


if __name__ == '__main__':
    I = Initiation()
    main()
else:
    I = Initiation()
