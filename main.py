from queue import Queue
import json
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
        self.points = 0
        self.duration = 0
        self.time_left = 10
        self.lvl = 0
        self.game_end = 0
        self.abort = 0
        self.print_lock = threading.Lock()
        self.time_left_lock = threading.Lock()
        self.leaderboard = 'leaderboard'


def timer():
    time.sleep(1)
    with I.time_left_lock:
        I.time_left -= 1
    I.duration += 1
    if I.time_left == 0:
        message("\nTime's up!")
        I.game_end = 1


def game():
    nt = task()                                             # generate new task
    while 1:
        try:
            user = int(input(nt[0])[0:5])
            if check_answer(user,nt[1]) == 1 or I.time_left == 0:
                break
        except ValueError:
            message('Only numbers!')
            if I.time_left == 0:
                break
        except (KeyboardInterrupt, EOFError):
            message('\nAbort!')
            I.game_end = 1
            I.abort = 1
            return


def task():
    o = ('+', '-')
    operation = {
        '+': (lambda x,y: x + y),
        '-': (lambda x,y: x - y),
        '*': (lambda x,y: x * y),
        '/': (lambda x,y: x / y)
    }
    max = {0:11,1:51,2:31,3:61,4:101,5:11,6:(11,11,51),7:(21,11,51),8:(16,51)}[I.lvl]
    a = r.randrange(1,max) if I.lvl in (0,1,2,3,4,5) else r.randrange(1,max[0])
    b = r.randrange(1,max) if I.lvl in (0,1,2,3,4,5) else r.randrange(1,max[1]) if I.lvl in (6, 7) else r.randrange(1,max[0])
    c = r.randrange(1,max) if I.lvl in (0,1,2,3,4,5) else r.randrange(1,max[2]) if I.lvl in (6, 7) else r.randrange(1,max[1])
    d = r.randrange(1,max[1]) if I.lvl is 8 else 0
    o1 = r.choice(o)
    o2 = r.choice(o)
    if I.lvl in (0,1):                                      # a +|- b
        text = '{a} {o1} {b} = '.format(a=a,b=b,o1=o1)
        answer = operation[o1](a,b)
    elif I.lvl in (2,3,4):                                  # a +|- b +|- c
        text = '{a} {o1} {b} {o2} {c} = '.format(a=a,b=b,c=c,o1=o1,o2=o2)
        answer = operation[o2](operation[o1](a,b),c)
    elif I.lvl is 5:                                        # a * b
        text = '{a} * {b} = '.format(a=a,b=b)
        answer = operation['*'](a,b)
    elif I.lvl in (6, 7):                                   # a * b +|- c
        text = '{a} * {b} {o1} {c} = '.format(a=a,b=b,c=c,o1=o1)
        answer = operation[o1](operation['*'](a,b),c)
    elif I.lvl is 8:                                        # a * b +|- c +|- d
        text = '{a} * {b} {o1} {c} {o2} {d} = '.format(a=a,b=b,c=c,d=d,o1=o1,o2=o2)
        answer = operation[o2](operation[o1](operation['*'](a,b),c),d)
    return (text,answer)


def check_answer(user,answer):
    if user == answer:
        msg = 'Correct! Time left: {} sec. Combo: {}'.format(I.time_left, I.combo)
        message(msg,1)
        reward(1)
        return 1
    if I.time_left != 0:
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
        elif I.lvl is 5:
            point_plus = 10 if I.combo < 2 else 10 * I.combo
            time_plus = 3
        elif I.lvl in (6,7):
            point_plus = 15 if I.combo < 2 else 15 * I.combo
            time_plus = 5
        elif I.lvl is 8:
            point_plus = 30 if I.combo < 2 else 30 * I.combo
            time_plus = 8
        with I.time_left_lock:
            I.time_left += time_plus
        I.points += point_plus
        I.combo += 1 if I.combo < I.combo_limit else 0
        I.combo_max = I.combo if I.combo >= I.combo_max else I.combo_max
        if I.combo_max in (5,10,15,20,25,30,35,40):
            I.lvl = {5: 1, 10: 2, 15: 3, 20: 4, 25: 5, 30: 6, 35: 7, 40: 8}[I.combo_max]


def game_over():
    msg = """
┏━━━━━━━━━━┓
┃ ==== Game Over ==== ┃
┣━━━━━━━━━━┫
┃ Max Combo:        {}┃
┃ Duration:        {}┃
┃ Points:    {}┃
┗━━━━━━━━━━┛
""".format(str(I.combo_max).zfill(2), str(I.duration).zfill(3), str(I.points).zfill(9))
    message(msg,1)
    if I.abort != 1:
        return leaderboard()


def leaderboard():
    try:
        content = json.load(open(I.leaderboard))
    except (FileNotFoundError, ValueError):
        try:
            json.dump({'9': {'name': 'Cirno'}},fp=open(I.leaderboard,'w'),indent=3)
            content = json.load(open(I.leaderboard))
        except FileNotFoundError:
            return
    if I.points > 0 and (I.points > min(map(lambda x: int(x), content)) or len(content) < 5):
        if len(content) == 5:
            del content[str(min(map(lambda x: int(x), content)))]
        name = input('New highscore!\nEnter your name: ')[0:15]
        content[str(I.points)] = {'name': name}
        json.dump(content,fp=open(I.leaderboard,'w'),indent=3)
    for i in reversed(sorted(map(lambda x: int(x), content))):
        print('{} - {}'.format(str(i).zfill(9),content[str(i)]['name']))


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
