import unittest
import main as m


class check_answer(unittest.TestCase):
    def test_correct(self):
        answer = 4
        x = 2
        y = 2
        self.assertEqual(m.check_answer(answer,x,y), 1)
        self.assertEqual(m.get_points(), 1)
        m.I.points = 0

    def test_wrong(self):
        answer = 5
        x = 2
        y = 2
        self.assertEqual(m.check_answer(answer,x,y), 0)
        self.assertEqual(m.get_points(), 0)

if __name__ == '__main__':
    unittest.main()
