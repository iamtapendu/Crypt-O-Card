import cv2 as cv
import datetime as dt

class Card:
    def __init__(self):
        self.img = None
        self.width = 0
        self.height = 0

    def uploadCard(self, path):
        self.img = cv.imread(path, 1)
        self.width = self.img.shape[0]
        self.height = self.img.shape[1]

    def displayCard(self):
        cv.imshow('hello', self.img)
        key = cv.waitKey(0)
        if (key == ord('q')):
            cv.destroyAllWindows()

    def saveCard(self):
        now = dt.datetime.now()
        cv.imwrite("Encrypted/Encrypt-O-Card_"+now.strftime('%d-%m-%Y_%X')+".png",self.img)


if __name__ == '__main__':
    card = Card()

    card.uploadCard('Images/profilePhoto.jpg')
    card.img[150:450, 250:451, 0] = 255
    card.displayCard()
    card.saveCard()
    print(card.img[1,643,0])