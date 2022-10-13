import sys
from io import StringIO
from unittest import TestCase, main
from unittest.mock import patch

import numpy as np

import Hamming


class makeH(TestCase):
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


class makeG(TestCase):
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


class makeR(TestCase):
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


class sendMessage(TestCase):
    def test_D_is_1(self):
        __stdout__ = sys.stdout
        sys.stdout = StringIO()

        np.random.seed(0)
        x = Hamming.sendMessage(1)
        correct = np.array([0, 0, 0])
        self.assertIsNone(np.testing.assert_array_equal(x, correct))

        sys.stdout = __stdout__

    def test_D_is_2(self):
        __stdout__ = sys.stdout
        sys.stdout = StringIO()

        np.random.seed(0)
        x = Hamming.sendMessage(2)
        correct = np.array([1, 0, 0, 1, 1])
        self.assertIsNone(np.testing.assert_array_equal(x, correct))

        sys.stdout = __stdout__

    def test_D_is_3(self):
        __stdout__ = sys.stdout
        sys.stdout = StringIO()

        np.random.seed(0)
        x = Hamming.sendMessage(3)
        correct = np.array([1, 1, 0, 0, 1, 1])
        self.assertIsNone(np.testing.assert_array_equal(x, correct))

        sys.stdout = __stdout__

    def test_D_is_4(self):
        __stdout__ = sys.stdout
        sys.stdout = StringIO()

        np.random.seed(0)
        x = Hamming.sendMessage(4)
        correct = np.array([1, 1, 0, 0, 1, 1, 0])
        self.assertIsNone(np.testing.assert_array_equal(x, correct))

        sys.stdout = __stdout__


class errorCorrect(TestCase):
    def test_r_has_0_errors(self):
        __stdout__ = sys.stdout
        sys.stdout = StringIO()

        D = np.random.randint(26)
        x = Hamming.sendMessage(D)
        r = Hamming.errorCorrect(x)
        self.assertIsNone(np.testing.assert_array_equal(x, r))

        sys.stdout = __stdout__

    def test_r_has_1_error(self):
        __stdout__ = sys.stdout
        sys.stdout = StringIO()

        D = np.random.randint(26)
        x = Hamming.sendMessage(D)
        rand = np.random.randint(len(x))
        x[rand] = not x[rand]
        r = Hamming.errorCorrect(x)
        self.assertIsNone(np.testing.assert_array_equal(x, r))

        sys.stdout = __stdout__


class receiveMessage(TestCase):
    def test(self):
        __stdout__ = sys.stdout
        sys.stdout = StringIO()

        np.random.seed(0)
        D = np.random.randint(26)
        x = Hamming.sendMessage(D)
        p = Hamming.receiveMessage(x)
        correct = np.array([1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0])
        self.assertIsNone(np.testing.assert_array_equal(p, correct))

        sys.stdout = __stdout__


class testMain(TestCase):
    @patch('builtins.input', side_effect=['1'])
    def test_d_is_1(self, _):
        np.random.seed(0)

        __stdout__ = sys.stdout
        capturedOutput = StringIO()
        sys.stdout = capturedOutput

        Hamming.main()

        sys.stdout = __stdout__

        correct = ("Message          : [0]\n"
                   "Send Vector      : [0 0 0]\n"
                   "Received Message : [0 1 0]\n"
                   "Parity Check     : [0 1]\n"
                   "Corrected Message: [0 0 0]\n"
                   "Decoded Message  : [0]\n")

        self.assertEqual(capturedOutput.getvalue(), correct)

    @patch('builtins.input', side_effect=['4'])
    def test_d_is_4(self, _):
        np.random.seed(0)

        __stdout__ = sys.stdout
        capturedOutput = StringIO()
        sys.stdout = capturedOutput

        Hamming.main()

        sys.stdout = __stdout__

        correct = ("Message          : [0 1 1 0]\n"
                   "Send Vector      : [1 1 0 0 1 1 0]\n"
                   "Received Message : [1 1 0 1 1 1 0]\n"
                   "Parity Check     : [0 0 1]\n"
                   "Corrected Message: [1 1 0 0 1 1 0]\n"
                   "Decoded Message  : [0 1 1 0]\n")

        self.assertEqual(capturedOutput.getvalue(), correct)

    @patch('builtins.input', side_effect=['0', '1'])
    def test_d_is_0(self, _):
        np.random.seed(0)

        __stdout__ = sys.stdout
        capturedOutput = StringIO()
        sys.stdout = capturedOutput

        Hamming.main()

        sys.stdout = __stdout__

        correct = ("\n"
                   "Must be a positive integer!\n"
                   "Message          : [0]\n"
                   "Send Vector      : [0 0 0]\n"
                   "Received Message : [0 1 0]\n"
                   "Parity Check     : [0 1]\n"
                   "Corrected Message: [0 0 0]\n"
                   "Decoded Message  : [0]\n")

        self.assertEqual(capturedOutput.getvalue(), correct)

    @patch('builtins.input', side_effect=['-3.14', '1'])
    def test_d_is_neg_3_14(self, _):
        np.random.seed(0)

        __stdout__ = sys.stdout
        capturedOutput = StringIO()
        sys.stdout = capturedOutput

        Hamming.main()

        sys.stdout = __stdout__

        correct = ("\n"
                   "Must be a positive integer!\n"
                   "Message          : [0]\n"
                   "Send Vector      : [0 0 0]\n"
                   "Received Message : [0 1 0]\n"
                   "Parity Check     : [0 1]\n"
                   "Corrected Message: [0 0 0]\n"
                   "Decoded Message  : [0]\n")

        self.assertEqual(capturedOutput.getvalue(), correct)


if __name__ == '__main__':
    main()
