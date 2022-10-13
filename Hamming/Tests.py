import unittest

import numpy as np

import Hamming


class makeH(unittest.TestCase):
    def test_D_is_1(self):
        H = Hamming.makeH(2, 1)
        correct = np.array([
            [1, 0, 1],
            [0, 1, 1]
        ])
        self.assertIsNone(np.testing.assert_array_equal(H, correct))

    def test_D_is_2(self):
        H = Hamming.makeH(3, 2)
        correct = np.array([
            [1, 0, 1, 0, 1],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 1, 1]
        ])
        self.assertIsNone(np.testing.assert_array_equal(H, correct))

    def test_D_is_3(self):
        H = Hamming.makeH(3, 3)
        correct = np.array([
            [1, 0, 1, 0, 1, 0],
            [0, 1, 1, 0, 0, 1],
            [0, 0, 0, 1, 1, 1]
        ])
        self.assertIsNone(np.testing.assert_array_equal(H, correct))

    def test_D_is_4(self):
        H = Hamming.makeH(3, 4)
        correct = np.array([
            [1, 0, 1, 0, 1, 0, 1],
            [0, 1, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 1]
        ])
        self.assertIsNone(np.testing.assert_array_equal(H, correct))


class makeG(unittest.TestCase):
    def test_D_is_1(self):
        G = Hamming.makeG(2, 1)
        correct = np.array([
            [1],
            [1],
            [1]
        ])
        self.assertIsNone(np.testing.assert_array_equal(G, correct))

    def test_D_is_2(self):
        G = Hamming.makeG(3, 2)
        correct = np.array([
            [1, 1],
            [1, 0],
            [1, 0],
            [0, 1],
            [0, 1]
        ])
        self.assertIsNone(np.testing.assert_array_equal(G, correct))

    def test_D_is_3(self):
        G = Hamming.makeG(3, 3)
        correct = np.array([
            [1, 1, 0],
            [1, 0, 1],
            [1, 0, 0],
            [0, 1, 1],
            [0, 1, 0],
            [0, 0, 1]
        ])
        self.assertIsNone(np.testing.assert_array_equal(G, correct))

    def test_D_is_4(self):
        G = Hamming.makeG(3, 4)
        correct = np.array([
            [1, 1, 0, 1],
            [1, 0, 1, 1],
            [1, 0, 0, 0],
            [0, 1, 1, 1],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        self.assertIsNone(np.testing.assert_array_equal(G, correct))


class makeR(unittest.TestCase):
    def test_D_is_1(self):
        R = Hamming.makeR(2, 1)
        correct = np.array([
            [0, 0, 1]
        ])
        self.assertIsNone(np.testing.assert_array_equal(R, correct))

    def test_D_is_2(self):
        R = Hamming.makeR(3, 2)
        correct = np.array([
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1]
        ])
        self.assertIsNone(np.testing.assert_array_equal(R, correct))

    def test_D_is_3(self):
        R = Hamming.makeR(3, 3)
        correct = np.array([
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]
        ])
        self.assertIsNone(np.testing.assert_array_equal(R, correct))

    def test_D_is_4(self):
        R = Hamming.makeR(3, 4)
        correct = np.array([
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 1]
        ])
        self.assertIsNone(np.testing.assert_array_equal(R, correct))


class sendMessage(unittest.TestCase):
    def test_D_is_1(self):
        np.random.seed(0)
        x = Hamming.sendMessage(1)
        correct = np.array([0, 0, 0])
        self.assertIsNone(np.testing.assert_array_equal(x, correct))

    def test_D_is_2(self):
        np.random.seed(0)
        x = Hamming.sendMessage(2)
        correct = np.array([1, 0, 0, 1, 1])
        self.assertIsNone(np.testing.assert_array_equal(x, correct))

    def test_D_is_3(self):
        np.random.seed(0)
        x = Hamming.sendMessage(3)
        correct = np.array([1, 1, 0, 0, 1, 1])
        self.assertIsNone(np.testing.assert_array_equal(x, correct))

    def test_D_is_4(self):
        np.random.seed(0)
        x = Hamming.sendMessage(4)
        correct = np.array([1, 1, 0, 0, 1, 1, 0])
        self.assertIsNone(np.testing.assert_array_equal(x, correct))


class errorCorrect(unittest.TestCase):
    def test_r_has_0_errors(self):
        np.random.seed(0)
        D = np.random.randint(26)
        x = Hamming.sendMessage(D)
        r = Hamming.errorCorrect(x)
        self.assertIsNone(np.testing.assert_array_equal(x, r))

    def test_r_has_1_error(self):
        np.random.seed(0)
        D = np.random.randint(26)
        x = Hamming.sendMessage(D)
        rand = np.random.randint(len(x))
        x[rand] = not x[rand]
        r = Hamming.errorCorrect(x)
        self.assertIsNone(np.testing.assert_array_equal(x, r))


if __name__ == '__main__':
    unittest.main()
