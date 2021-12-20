#     Crypt-O-Card encrypt and decrypt text message into an image file
#     Copyright (C) 2021 Tapendu Karmakar
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import numpy
import Card
import hashlib

SIGN = 'Crypt-O-Card'
SIGN_LEN = len(SIGN) * 8
TEXT_LEN = 16


class Capsule:
    def __init__(self):
        self.text = ''
        self.card = Card.Card()
        self.password = ''

    def setText(self, text):
        self.text = text.strip()

    def getText(self):
        return self.text

    def setPassword(self, text):
        if (len(text) > 4 and len(text) <= 32):
            hashCode = hashlib.md5(text.encode())
            self.password = hashCode.hexdigest()
            return True
        return False

    def getPassword(self):
        return self.password

    def charToBin(self, char):
        temp = ord(char)
        bin = ''
        for i in range(7, -1, -1):
            k = temp >> i
            if (k & 1):
                bin += '1'
            else:
                bin += '0'
        return bin

    def binToChar(self, bin):
        temp = int(bin, 2)
        return chr(temp)

    def putAtLSB(self, source, bit):
        if (source & 1 != bit):
            if (source < 255):
                source += 1
            else:
                source -= 1
        return source

    def getFromLSB(self, source):
        return source % 2

    def writePassword(self):
        if (not len(self.password) > 4):
            return False

        x = SIGN_LEN + TEXT_LEN
        for letter in self.password:
            for bit in self.charToBin(letter):
                self.card.img[0, x, self.card.channel] = self.putAtLSB(self.card.img[0, x, self.card.channel], int(bit))
                x = (x + 1) % self.card.width

        return True

    def readPassword(self):
        if (not self.checkValidity()):
            return False

        x = SIGN_LEN + TEXT_LEN
        self.password = ''
        for letter in range(0, 32):
            bin = ''
            for i in range(8):
                bin += str(self.getFromLSB(self.card.img[0, x, self.card.channel]))
                x = (x + 1) % self.card.width
            self.password += self.binToChar(bin)

        return True

    def authenticate(self, pWord=''):
        if (len(pWord) > 4 and len(pWord) <= 16 and self.readPassword()):
            code = hashlib.md5(pWord.encode()).hexdigest()

            if (code == self.password):
                return True

        return False

    def writeTextProperties(self):
        if not ((len(self.text) > 3) and isinstance(self.card.img, numpy.ndarray)):
            return False

        x = 0

        for letter in SIGN:
            for bit in self.charToBin(letter):
                self.card.img[0, x, self.card.channel] = self.putAtLSB(self.card.img[0, x, self.card.channel], int(bit))
                x = (x + 1) % self.card.width

        temp = len(self.text)
        bin = ''
        for i in range(15, -1, -1):
            k = temp >> i
            if (k & 1):
                bin += '1'
            else:
                bin += '0'

        for bit in bin:
            self.card.img[0, x, self.card.channel] = self.putAtLSB(self.card.img[0, x, self.card.channel], int(bit))
            x = (x + 1) % self.card.width

        if (not self.writePassword()):
            return False

        return True

    def checkValidity(self):
        tmpSign = ''
        x = 0
        for letter in range(0, len(SIGN)):
            bin = ''
            for i in range(8):
                bin += str(self.getFromLSB(self.card.img[0, x, self.card.channel]))
                x = (x + 1) % self.card.width
            tmpSign += self.binToChar(bin)

        if (tmpSign == SIGN):
            return True
        return False

    def readTextProperties(self):
        if (not self.checkValidity()):
            return 0
        bin = ''
        for x in range(SIGN_LEN, SIGN_LEN + TEXT_LEN):
            bin += str(self.getFromLSB(self.card.img[0, x, self.card.channel]))
        return int(bin, 2)

    def combineCardWithText(self):
        if (not self.writeTextProperties()):
            return False

        x, y = 0, 1
        for letter in self.text:
            for bit in self.charToBin(letter):
                self.card.img[y, x, self.card.channel] = self.putAtLSB(self.card.img[y, x, self.card.channel], int(bit))
                y = y + (x + 1) // self.card.width
                x = (x + 1) % self.card.width
                if (y == self.card.height and self.card.channel != 3):
                    x = y = 0
                    self.card.channel += 1

        return True

    def separateCardFromText(self, password):
        self.text = ''
        x, y = 0, 1
        length = self.readTextProperties()
        if (len == 0):
            return False
        if (not self.authenticate(password)):
            return False

        for letter in range(length):
            bin = ''
            for i in range(8):
                bin += str(self.getFromLSB(self.card.img[y, x, self.card.channel]))
                y = y + (x + 1) // self.card.width
                x = (x + 1) % self.card.width
            self.text += self.binToChar(bin)

        return True


if __name__ == '__main__':
    cap = Capsule()
    # print('A = ', cap.charToBin('A'))
    # print('1000001 = ', cap.binToChar('1000001'))
    # print(cap.getFromLSB(254))

    # for i in cap.charToBin('A'):
    #    print(cap.putAtLSB(254,int(i)))
    cap.card.uploadCard('Images/profilePhoto.jpg')

    text = '''Theory of Programming is a very helpful website that helps you in understanding
     a wide range of programming concepts. There are many posts on Data Structures, Algorithms
      and the Java Programming Language which explain the concepts with vivid explanations, 
      well-drawn diagrams and also come with the actual code of concept. Theory of Programming 
      also has posts on solving competitive coding questions which are based on data structures 
      and algorithms discussed in the website. These help you not only to be a hero in your classroom 
      but also a legend in the coding websites such as CodeChef, SPOJ, etc.'''

    cap.setText(text)

    # cap.writeTextProperties()
    # print(cap.readTextProperties())

    cap.setPassword('T@pendu2001')
    # cap.writePassword()
    # cap.readPassword()
    # print(cap.getPassword())

    # a = hashlib.md5('T@pendu2001'.encode())
    # print(a.hexdigest())
    #
    cap.combineCardWithText()
    cap.separateCardFromText('T@pendu2001')
    print(cap.getText())
    print(cap.checkValidity())

    cap.card.displayCard()
