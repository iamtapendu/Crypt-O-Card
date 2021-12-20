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

import cv2 as cv
import datetime as dt


class Card:
    def __init__(self):
        self.img = None
        self.width = 0
        self.height = 0
        self.channel = 0

    def uploadCard(self, path):
        img = cv.imread(path, 1)
        if (img.shape[1] >= 370):
            self.width = img.shape[1]
            self.height = img.shape[0]
            self.img = img

    def saveCard(self):
        now = dt.datetime.now()
        cv.imwrite("Encrypted/Encrypt-O-Card_" + now.strftime('%d-%m-%Y_%X') + ".png", self.img)


if __name__ == '__main__':
    card = Card()

    card.uploadCard('Images/profilePhoto.jpg')
    card.img[150:450, 250:451, 0] = 255
    card.displayCard()
    card.saveCard()
    print(card.img[1, 643, 0])
