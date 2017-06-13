import unittest
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


class task(unittest.TestCase):
    def setUp(self):
        m.I.__init__()

    def test_task_new_lvl_0_1(self):
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
        self.assertEqual(m.I.combo, 1)
        self.assertEqual(m.I.combo_max, 1)

    def test_reward_gain_vlv4(self):
        m.I.lvl = 4
        m.reward(1)
        self.assertEqual(m.I.points, 5)
        self.assertEqual(m.I.time_left, 12)
        self.assertEqual(m.I.combo, 1)
        self.assertEqual(m.I.combo_max, 1)

    def test_reward_gain_combo_max(self):
        m.I.combo = 20
        m.reward(1)
        self.assertEqual(m.I.combo, 20)
        self.assertEqual(m.I.lvl, 4)


if __name__ == '__main__':
    unittest.main()
