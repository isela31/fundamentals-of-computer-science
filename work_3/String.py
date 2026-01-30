class Base64DecodeError(Exception):
    def __str__(self):
        return "can't decode from base 64"


class CyclicCharsError(Exception):
    def __str__(self):
        return "can't decode"


class BytePairError(Exception):
    pass


class BytePairDecodeError(Exception):
    pass


class String():
    def __init__(self, string: str):
        self.string = string
        self.i = -1
        self.rules = []

    def __str__(self):
        return self.string

    def __add__(self, other):

        return String(self.string + other.string)

    def __radd__(self, other):
        return String(other.string + self.string)

    def __mul__(self, other):
        return String(self.string * other)

    def __rmul__(self, other):
        return String(self.string*other)

    def __eq__(self, other):
        if isinstance(other, String):
            return self.string == other.string
        if isinstance(other, str):
            return self.string == other

    def isupper(self):
        return self.string.isupper()

    def islower(self):
        return self.string.islower()

    def count(self, sub):
        return self.string.count(sub.string)

    def __getitem__(self, item):
        return self.string[item]

    def __iter__(self):
        self.i = -1
        return self

    def __next__(self):
        self.i += 1
        return self.string[self.i]

    def __len__(self):
        return len(self.string)

    def base64(self) -> 'String':
        '''
        Encode the String (self) to a base64 string
        :return: a new instance of String with the encoded string.
        '''
        res = ''.join(format(ord(i), '08b') for i in self.string)  # change the String to binary sequence

        while len(res) % 6 != 0:  # padding
            res = res + '0'

        chunks = [res[i:i + 6] for i in range(0, len(res), 6)]  # convert the string to list in chuncks of 6

        list = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

        for i in range(len(chunks)):
            x = int(chunks[i], 2)
            chunks[i] = list[x]

        H = ""
        for j in chunks:
            H += j

        return String(H)

    def byte_pair_encoding(self):
        '''
        Encode the String (self) to a byte pair string
        :return: a new instance of String with the encoded string.
        :exception: BytePairError
        '''

        groups_dict = {'other': list("!\"#$%&'()*+,-./:;<=>?@[\]^_`|}~"),
                       'digits': list('0123456789'), 'upper_case': list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                       'lower_case': list('abcdefghijklmnopqrstuvwxyz')}

        others = False
        Digits = False
        Upper_case = False
        lower_case = False

        for i in self.string:
            if 32 < ord(i) < 48 or 57 < ord(i) < 65 or 90 < ord(i) < 97 or 123 < ord(i) < 127:
                others = True
            if (48 <= ord(i) <=57):
                Digits = True
            if (65 <= ord(i) <=90):
                Upper_case = True
            if (97<=ord(i) <= 122):
                lower_case = True
        if others:
            groups_dict.pop('other')
        if Digits:
            groups_dict.pop('digits')
        if Upper_case:
            groups_dict.pop('upper_case')
        if lower_case:
            groups_dict.pop('lower_case')

        values = groups_dict.values()
        c = []
        for item in values:
            c += item

        if len(c)< 1:
            raise BytePairError
        stoper = False
        string1 = self.string
        rules = []

        while not stoper:
            pairs = [string1[i:i + 2] for i in range(len(string1) - 1)]
            dict = {pair: string1.count(pair) for pair in pairs}
            e = dict.values()
            stoper = True
            for i in e:
                if i != 1:
                    stoper = False
            if stoper:
                break
            max_key = max(dict, key=dict.get)
            try:
                string1 = string1.replace(max_key, c[0])
            except IndexError:
                raise BytePairError

            rules.append(f'{c[0]} = {max_key}')
            c.pop(0)

        x = String(string1)
        x.rules = rules
        return x

    def cyclic_bits(self, num: int) -> 'String':
        '''
        Encode the String (self) to a cyclic bits string
        :return: a new instance of String with the encoded string.
        '''
        num = num % (len(self.string) * 8)
        bin_string = ''.join(format(ord(i), '08b') for i in self.string)

        x = list(bin_string)
        for i in range(len(bin_string)):
            if i + num < len(bin_string):
                x[len(bin_string) - 1 - (i + num)] = bin_string[len(bin_string) - 1 - i]
            if i + num >= len(bin_string):
                y = i + num - len(bin_string)
                x[i] = bin_string[y]

        cyclic_bin = ""

        chunks = [x[i:i + 8] for i in range(0, len(x), 8)]
        new_list = []
        for list1 in chunks:
            c = ("")
            for i in list1:
                c += i
            new_list.append(c)

        for bin in new_list:
            asci_integer = int(bin, 2)
            asci_chr = chr(asci_integer)
            cyclic_bin += asci_chr

        return String(cyclic_bin)

    def cyclic_chars(self, num: int) -> 'String':
        '''
        Encode the String (self) to a cyclic chars string
        :return: a new instance of String with the encoded string.
        :exception: CyclicCharsError
        '''
        empty_string = ""
        if not self.string.isprintable():
            raise CyclicCharsError

        for c in self.string:
            j = ord(c) + num
            while j > 126:
                j = j - 95
            while j < 32:
                j = j + 95
            k = chr(j)
            empty_string += k

        return String(empty_string)


    def histogram_of_chars(self) -> dict:
        '''
        calculate the histogram of the String (self). The bins are
        "control code", "digits", "upper", "lower" , "other printable"
        and "higher than 128".
        :return: a dictonery of the histogram. keys are bins.
        '''
        dict = {"control code":0,"digits":0,"upper":0,"lower":0,"other printable":0,"higher than 128":0}
        control_code = 0
        digits = 0
        upper = 0
        lower = 0
        others = 0
        higer = 0
        for i in self.string:
            if 0<=ord(i)<32 or ord(i)==127:
                control_code+=1
            if 48<=ord(i)<=57:
                digits += 1
            if 65<=ord(i)<=90:
                upper+=1
            if 97 <= ord(i) <= 122:
                lower += 1
            if 32 <= ord(i) < 48 or 57 < ord(i) < 65 or 90 < ord(i) < 97 or 123 < ord(i) < 127:
                others += 1
            if 127<ord(i)<=255:
                higer += 1
        dict["control code"] = control_code
        dict["digits"] = digits
        dict["upper"] = upper
        dict["lower"] = lower
        dict["other printable"] = others
        dict["higher than 128"] = higer

        return dict

    def decode_base64(self) -> 'String':
        '''
        Decode the String (self) to its original base64 string.
        :return: a new instance of String with the endecoded string.
        :exception: Base64DecodeError
        '''
        list = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        list1 = []
        for i in range(len(self.string)):  # create list with the Sextets
            if not (self.string[i] in list):
                raise Base64DecodeError
            x = list.index(self.string[i])
            list1.append(x)

        list2 = []
        for num in list1:  # convert each sextets to binary
            x = bin(num).replace("0b", "")
            x = x.rjust(6, "0")
            list2.append(x)

        binary = ""  # convert the binary list to string
        for i in list2:
            binary += i

        chunks = [binary[i:i + 8] for i in range(0, len(binary), 8)]  # chuncks to bits  of 8 and convert to list

        if len(chunks[-1]) < 8:
            x = int(chunks[-1])
            if x != 0:
                raise Base64DecodeError # i workd by this algoritem : base64.guru/learn/base64-algorithm/decode
            chunks.pop()

        asci = ""
        for i in chunks:
            asci_integer = int(i, 2)
            asci_chr = chr(asci_integer)

            asci += asci_chr

        return String(asci)

    def decode_byte_pair(self) -> 'String':
        '''
        Decode the String (self) to its original byte pair string.
        Uses the hoproperty rules.
        :return: a new instance of String with the endecoded string.
        :exception: BytePairDecodeError
        '''
        rules = self.rules

        if len(self.rules) < 1 :
            raise BytePairDecodeError

        string1 = self.string
        for i in reversed(rules):
            for j in string1:
                if j == i[0]:
                    string1 = string1.replace(j, i[4]+i[5])
            rules.pop(-1)


        string2 = String(string1)
        string2.rules = rules

        return string2


    def decode_cyclic_bits(self, num: int) -> 'String':
        '''
        Decode the String (self) to its original cyclic bits string.
        :return: a new instance of String with the endecoded string.
        '''
        num = num % (len(self.string) * 8)
        bin_string = ''.join(format(ord(i), '08b') for i in self.string)

        x = list(bin_string)
        for i in range(len(bin_string)):
            if i + num < len(bin_string):
                x[i + num] = bin_string[i]
            if i + num >= len(bin_string):
                y = i + num - len(bin_string)
                x[y] = bin_string[i]

        cyclic_bin = ""

        chunks = [x[i:i + 8] for i in range(0, len(x), 8)]
        new_list = []
        for list1 in chunks:
            c = ("")
            for i in list1:
                c += i
            new_list.append(c)

        for bin in new_list:
            asci_integer = int(bin, 2)
            asci_chr = chr(asci_integer)
            cyclic_bin += asci_chr

        return String(cyclic_bin)

    def decode_cyclic_chars(self, num: int) -> 'String':
        '''
        Decode the String (self) to its original cyclic chars string.
        :return: a new instance of String with the endecoded string.
        :exception: CyclicCharsDecodeError
        '''
        empty_string = ""
        for i in range(len(self.string)):
            if ord(self.string[i]) < 32 or ord(self.string[i]) > 126:
                raise CyclicCharsError
            j = ord(self.string[i]) - num
            while j < 32:
                j = j + 95
            while j > 126:
                j = j - 95
            k = chr(j)
            empty_string += k

        return String(empty_string)
