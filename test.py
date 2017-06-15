import os
import unittest
from unittest.mock import patch
import main as m


class timer(unittest.TestCase):
    def setUp(self):
        m.I.__init__()

    def test_timer_count(self):
        m.I.time_left = 1
        m.timer()
        self.assertEqual(m.I.time_left, 0)
        self.assertEqual(m.I.duration, 1)
        self.assertEqual(m.I.game_end, 1)


class game(unittest.TestCase):
    def setUp(self):
        m.I.__init__()

    @patch('__main__.m.task', return_value=('msg',1))
    @patch('__main__.m.input', return_value='1')
    def test_game_correct(self,nt,input):
        m.game()
        self.assertEqual(m.I.points, 1)

    @patch('__main__.m.task', return_value=('msg',1))
    @patch('__main__.m.input', return_value='some')
    def test_game_raise_ValueError(self,nt,input):
        m.I.time_left = 0
        self.assertRaises(ValueError, m.game())


class task(unittest.TestCase):
    def setUp(self):
        m.I.__init__()

    def test_task_new(self):
        lvl = (0,2,5,6,8)
        for i in lvl:
            m.I.lvl = i
            n = m.task()
            self.assertEqual(len(m.task()), 2)
            self.assertEqual(type(n[0]), str)
            self.assertEqual(type(n[1]), int)


class answer(unittest.TestCase):
    def setUp(self):
        m.I.__init__()

    def test_answer_correct(self):
        user = 4
        answer = 4
        self.assertEqual(m.check_answer(user,answer), 1)
        self.assertEqual(m.I.points, 1)

    def test_answer_wrong(self):
        user = 4
        answer = 5
        self.assertEqual(m.check_answer(user,answer), 0)
        self.assertEqual(m.I.points, 0)


class reward(unittest.TestCase):
    def setUp(self):
        m.I.__init__()

    def test_reward_lose(self):
        m.I.combo = 5
        m.I.combo_max = 99
        m.I.points = 5
        m.reward()
        self.assertEqual(m.I.combo, 0)
        self.assertEqual(m.I.combo_max, 99)
        self.assertEqual(m.I.points, 5)

    def test_reward_gain_vlv0(self):
        m.reward(1)
        self.assertEqual(m.I.points, 1)
        self.assertEqual(m.I.time_left, 11)

    def test_reward_gain_vlv4(self):
        m.I.lvl = 4
        m.reward(1)
        self.assertEqual(m.I.points, 5)
        self.assertEqual(m.I.time_left, 12)

    def test_reward_gain_vlv5(self):
        m.I.lvl = 5
        m.reward(1)
        self.assertEqual(m.I.points, 10)
        self.assertEqual(m.I.time_left, 13)

    def test_reward_gain_vlv6(self):
        m.I.lvl = 6
        m.reward(1)
        self.assertEqual(m.I.points, 15)
        self.assertEqual(m.I.time_left, 15)

    def test_reward_gain_vlv8(self):
        m.I.lvl = 8
        m.reward(1)
        self.assertEqual(m.I.points, 30)
        self.assertEqual(m.I.time_left, 18)

    def test_reward_gain_combo_max(self):
        m.I.combo = 40
        m.reward(1)
        self.assertEqual(m.I.combo, 40)
        self.assertEqual(m.I.lvl, 8)


class game_over(unittest.TestCase):
    def setUp(self):
        m.I.__init__()

    @patch('__main__.m.leaderboard', return_value='Done!')
    def test_game_over(self, leaderboard):
        self.assertEqual(m.game_over(), 'Done!')


class leaderboard(unittest.TestCase):
    def setUp(self):
        m.I.__init__()

    @patch('__main__.m.print', return_value='')
    @patch('__main__.m.input', return_value='Cirno')
    def test_leaderboard_normal(self, print, input):
        m.I.leaderboard = 'leaderboard_test'
        m.I.points = 999
        m.leaderboard()
        self.assertTrue('999' in open('leaderboard_test').read())
        os.remove('leaderboard_test')

    @patch('__main__.m.print', return_value='')
    @patch('__main__.m.input', return_value='Cirno')
    def test_leaderboard_full(self, print, input):
        with open('leaderboard_test', 'w') as file:
            file.write("""
{
   "8": {
      "name": "Cirno"
   },
   "7": {
      "name": "Cirno"
   },
   "6": {
      "name": "Cirno"
   },
   "5": {
      "name": "Cirno"
   },
   "4": {
      "name": "Not Cirno"
   }
}
                """)
        m.I.leaderboard = 'leaderboard_test'
        m.I.points = 999
        m.leaderboard()
        self.assertFalse('Not Cirno' in open('leaderboard_test').read())
        os.remove('leaderboard_test')

    @patch('__main__.m.print', return_value='')
    @patch('__main__.m.input', return_value='Cirno')
    def test_leaderboard_FileNotFoundError(self, print, input):
        m.I.leaderboard = ''
        self.assertRaises(FileNotFoundError, m.leaderboard())


if __name__ == '__main__':
    unittest.main()
