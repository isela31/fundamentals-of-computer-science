from typing import List


class Path:
    def __init__(self, distance=-1, word=''):
        self.distance = distance
        self.word = word

    def __lt__(self, other):
        if other.distance == -1:
            return True
        if self.distance == -1:
            return False
        return self.distance < other.distance


class State:
    def __init__(self, current: tuple, generators: tuple):
        self.current = current
        self.generators = generators
        self.zero, self.one = self.calc(0), self.calc(1)

    def calc(self, bit: int):

        next_state = (bit,) + self.current[:-1]
        curr_state = (bit,) + self.current
        output = []
        for g in self.generators:
            out = 0
            for i, ele in enumerate(g):
                if ele:
                    out ^= curr_state[i]
            output.append(out)

        return next_state, output


class ConvolutionalCode:
    """The code assumes zero state termination, and k=1"""

    def __init__(self, generators: tuple):
        self.generators = generators  # מספרים שמייצגים פולינומים

        self.gen = []  # הפולינומים הרלוונטיים
        temp_list = []
        for i in self.generators:
            temp_list.append((bin(i))[2:])

        Max = len((max(temp_list, key=len)))

        for poli in temp_list:
            if len(poli) < Max:
                a = poli.zfill(Max)
                b = a[::-1]
                self.gen.append(b)
            elif len(poli) == Max:
                c = poli[::-1]
                self.gen.append(c)

        self.gen = tuple([tuple(map(int, g)) for g in self.gen])

        self.L = Max - 1

        self.register = []  # המצב הנוכחי
        for i in range(self.L):
            self.register.append(0)

        """
        :param generators: each element in the tuple represents a single generator polynomial. The convention
        we use is: 1+D=b011=3 (and not 1+D=6)
        """

    def encode(self, data: bytes) -> List[int]:

        bin_str = ''

        for i in range(len(data)):
            bin_str += bin(data[i])[2:].zfill(8)

        bin_str += '0' * self.L
        output = []

        for d in bin_str:
            for poli in self.gen:
                if int(poli[0]) == 1:
                    a = int(d)
                    for num in range(1, len(poli)):
                        c = poli[num]
                        if c == 1:
                            a = a ^ int(self.register[num - 1])
                    output.append(int(a))

                else:
                    a = 0
                    for num in range(1, len(poli)):
                        if poli[num] == 1:
                            a = a ^ int(self.register[num - 1])
                    output.append(int(a))

            self.register = [d]+self.register[:-1]


        return output

        """
        encode input data bytes. Uses zero tail termination

        :param data: data to be encoded
        :return: encoded data
        :rtype: list[int]
        """

    def decode(self, data: List[int]):  # -> (bytes, int)

        n = len(self.gen)
        chuncks = [data[i:i + n] for i in range(0, len(data), n)]

        n = self.L
        states = []

        for i in range(1 << n):
            string = "{:0nb}"
            new_chr = str(n)
            string = string[:3] + new_chr + string[3 + 1:]
            a = string.format(i)
            b = State(tuple(map(int, a)), self.gen)
            states.append(b)

        states = tuple(states)
        paths = [Path() for _ in range(len(states))]
        paths[0].distance = 0

        for c in chuncks:
            new_paths = [Path() for _ in range(len(states))]
            for i, state in enumerate(states):
                path = paths[i]
                if path.distance == -1:
                    continue
                state0, out0 = state.zero
                word = path.word + '0'
                distance = path.distance
                for i, j in zip(c, out0):
                    if i != j:
                        distance += 1

                new_path = Path(distance, word)
                a = map(str, state0)
                b = ''.join(a)
                d = int(b, 2)
                new_paths[d] = min(new_paths[d], new_path)

                state1, out1 = state.one
                word = path.word + '1'
                distance = path.distance
                for i, j in zip(c, out1):
                    if i != j:
                        distance += 1

                new_path = Path(distance, word)
                a = map(str, state1)
                b = ''.join(a)
                d = int(b, 2)
                new_paths[d] = min(new_paths[d], new_path)

            paths = new_paths

        path = paths[0]

        f_path = path.word[:-self.L]
        final = [f_path[i * 8:(i + 1) * 8] for i in range((len(f_path) + 8 - 1) // 8)]
        final = bytes([int(i, 2) for i in final])


        return final, path.distance

        """
        decode data bytes. The function assumes initial and final state of encoder was at the zero state.

        :param data: coded data to be decoded, list of ints representing each received bit.
        :return: return a tuple of decoded data, and the amount of corrected errors.
        :rtype: (bytes, int)
        """

