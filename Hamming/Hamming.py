import numpy as np


def main():
    """
    Simulate Hamming code on random message of length D
    :return: Decoded message
    """
    D = int(float(input("Enter number of data bits:   ")))

    if D < 1:
        print("\nMust be a positive integer!")
        return main()

    x = sendMessage(D)
    return receiveMessage(x)


def makeH(n, D):
    """
    Create parity-check matrix
    :param n: Number of parity bits
    :param D: Number of message bits
    :return: Parity-check matrix H
    """
    H = np.zeros((n, n + D))

    for col in range(n + D):
        b = [int(d) for d in bin(col + 1).replace('0b', '')]
        for row in range(len(b)):
            H[row][col] = b[len(b) - row - 1]

    return H


def makeG(n, D):
    """
    Create a generator matrix
    :param n: Number of parity bits
    :param D: Number of message bits
    :return: Generator matrix G
    """
    H = makeH(n, D)
    for row in range(n - 1, -1, -1):
        H = np.delete(H, 2 ** row - 1, 1)

    G = np.zeros((2 ** n - 1, 2 ** n - n - 1))
    for row in range(n):
        for col in range(D):
            G[2 ** row - 1][col] = H[row][col]
        for i in range(2 ** row - 1):
            G[2 ** row + i][2 ** row + i - row - 1] = 1
    G = np.delete(G, np.s_[n + D:], axis=0)
    G = np.delete(G, np.s_[D:], axis=1)

    return G


def makeR(n, D):
    """
    Create a decoding matrix
    :param n: Number of parity bits
    :param D: Number of message bits
    :return: Decoding matrix R
    """
    R = np.zeros((2 ** n - n - 1, 2 ** n - 1))
    for row in range(n):
        for i in range(2 ** row - 1):
            R[2 ** row + i - row - 1][2 ** row + i] = 1
    R = np.delete(R, np.s_[D:], axis=0)
    R = np.delete(R, np.s_[n + D:], axis=1)

    return R


def sendMessage(D):
    """
    Create random message and encode it
    :param D: Length of un-encoded message
    :return: Encoded message vector
    """
    n = len(bin(D).replace('0b', ''))
    if 2 ** n - D <= n:
        n += 1

    p = np.random.randint(2, size=D)
    print("Message          :", p.astype(int))

    G = makeG(n, D)
    x = np.matmul(G, p) % 2
    print("Send Vector      :", x.astype(int))

    return x


def errorCorrect(r):
    """
    Check for parity and correct if error exists
    :param r: Message vector
    :return: Corrected message vector
    """
    n = len(bin(len(r)).replace('0b', ''))
    D = len(r) - n

    H = makeH(n, D)
    z = np.matmul(H, r) % 2
    print("Parity Check     :", z.astype(int))

    e = int('0b' + str(np.flip(z, axis=0)).replace('[', '').replace('.', '').replace(' ', '').replace(']', ''), 2) - 1
    if e >= 0:
        r[e] = not r[e]
        print("Corrected Message:", r.astype(int))

    return r


def receiveMessage(x):
    """
    Receive message, error correct, and decode
    :param x: Received message vector
    :return: Decoded message
    """
    r = x.copy()
    e = np.random.randint(-1, len(r))
    if e >= 0:
        r[e] = not r[e]
    print("Received Message :", r.astype(int))

    r = errorCorrect(r)

    n = len(bin(len(r)).replace('0b', ''))
    D = len(r) - n

    R = makeR(n, D)
    p = np.matmul(R, r) % 2
    print("Decoded Message  :", p.astype(int))

    return p


if __name__ == '__main__':
    main()
