import numpy as np


def main():
    D = int(float(input("Enter number of data bits:   ")))

    if D < 1:
        print("\nMust be a positive integer!")
        return main()

    n = len(bin(D).replace('0b', ''))
    if 2 ** n - D <= n:
        n += 1
    t = n + D

    H = np.zeros((n, t))
    for col in range(t):
        b = [int(d) for d in bin(col + 1).replace('0b', '')]
        for row in range(len(b)):
            H[row][col] = b[len(b) - row - 1]

    h = H.copy()
    for row in range(n - 1, -1, -1):
        h = np.delete(h, 2 ** row - 1, 1)

    G = np.zeros((2 ** n - 1, 2 ** n - n - 1))
    for row in range(n):
        for col in range(D):
            G[2 ** row - 1][col] = h[row][col]
        for i in range(2 ** row - 1):
            G[2 ** row + i][2 ** row + i - row - 1] = 1
    G = np.delete(G, np.s_[t:], axis=0)
    G = np.delete(G, np.s_[D:], axis=1)

    R = G.copy().transpose()
    for col in range(n):
        for row in range(D):
            R[row][2 ** col - 1] = 0

    p = np.random.randint(2, size=D)
    print("Message          :", p.astype(int))

    x = np.matmul(G, p) % 2
    print("Send Vector      :", x.astype(int))

    r = x.copy()
    rand = np.random.randint(t)
    r[rand] = not r[rand]
    print("Received Message :", r.astype(int))

    z = np.matmul(H, r) % 2
    print("Parity Check     :", z.astype(int))

    e = int('0b' + str(np.flip(z, axis=0)).replace('[', '').replace('.', '').replace(' ', '').replace(']', ''), 2) - 1
    r[e] = not r[e]
    print("Corrected Message:", r.astype(int))

    p = np.matmul(R, r) % 2
    print("Decoded Message  :", p.astype(int))


if __name__ == '__main__':
    main()
