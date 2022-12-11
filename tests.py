import unittest
from task_generator import generate_task, determinant


class messageTest(unittest.TestCase):
    def test_determinant(self):
        self.assertEqual(determinant([[1, 0, 2], [2, 0, 3], [4, 9, 6]]), 9)
        self.assertEqual(determinant([[8, 10, 0], [6, 4, 0], [6, 10, 0]]), 0)
        self.assertEqual(determinant([[10, 4, 6], [0, 6, 5], [2, 5, -3]]), -462)
        self.assertEqual(determinant([[6, 4], [4, 5]]), 14)

if __name__ == "__main__":
    unittest.main()
