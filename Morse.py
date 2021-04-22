from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import RPi.GPIO as GPIO
import sys
from time import sleep

xStart = 100
yStart = 100
wWidth = 400
wHeight= 300
pin = 12 #LED output pin
morseTimeUnit = 0.1 # standard time unit tio calculate di and da and gap

GPIO.setmode(GPIO.BCM) # use BCM as BOARD is the pin numbers which dont correlate to GPIO pins
GPIO.setup(pin, GPIO.OUT) # set pin to output mode

translationArray = [["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"],
                    [".-","-..","-.-.","-..",".","..-.","--.","....","..",".---","-.-",".-..","--","-.","---",".--.","--.-",".-.","...","-","..-","...-",".--","-..-","-.--","--.."]]
def Da(): # triger LED to perform Da
    #print("Da")
    GPIO.output(pin, GPIO.HIGH)
    sleep(morseTimeUnit*3)
    GPIO.output(pin, GPIO.LOW)
    
def Dit():# triger LED to perform Dit
    #print("Dit")
    GPIO.output(pin, GPIO.HIGH)
    sleep(morseTimeUnit)
    GPIO.output(pin, GPIO.LOW)
        
def CharGap():# intra character gap timing
    #print("gap")
    sleep(morseTimeUnit*3)
    
class MyWindow(QMainWindow): # class inherits from QMainWindow    
    def __init__(self): # contructor
        super(MyWindow, self).__init__()
        self.setGeometry(xStart, yStart, wWidth, wHeight)
        self.setWindowTitle("Morse Converter")    
        self.initUI()           
    
    def initUI(self): # use self.xxx to make it accessable anywhere in the class
        # Label1
        self.label1 = QtWidgets.QLabel(self) # added to self QMainWindow object
        self.label1.setText("Enter a max of 12 characters to translate to Morse")
        self.label1.move(10,10) # move label
        self.label1.adjustSize() # update the size of the label to fit the words
        
        # Text Area
        self.textEdit1 = QtWidgets.QTextEdit(self)
        self.textEdit1.setObjectName(u"textEdit1")
        self.textEdit1.setGeometry(20, 60, 231, 41)
        
        #ErrorLabel
        self.label2 = QtWidgets.QLabel(self) # added to self QMainWindow object
        self.label2.setText("")
        self.label2.move(10,200) # move label
        self.label2.adjustSize() # update the size of the label to fit the words          
        
        # Button 1
        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setObjectName(u"button1")
        self.button1.setGeometry(170, 130, 75, 23)
        self.button1.clicked.connect(self.buttonClickFunc) # link button to funciton buttonClickFunc
        self.button1.setText("Convert")      
    
    def buttonClickFunc(self): # button click function
        self.label2.setText("Starting: ")# reset the label text
        self.label2.adjustSize() 
        textAreaContents = self.textEdit1.toPlainText()# get text area text
        
        if len(textAreaContents) > 12: # if there are more than 12 characters
            self.label2.setText("ERROR: Exceeded 12 character limit") # change value in label
            self.label2.adjustSize() # update the size of the label to fit the words
        else:
            for i in range( len(textAreaContents) ):# loop through each character from the text box
                index = -1 # reset index each itteration
                try:
                    index = translationArray[0].index(textAreaContents[i].upper())# attempt to find it in my conversion array                 
                except:
                    self.label2.setText("ERROR: Invalid Character found") # change value in label
                    self.label2.adjustSize() # update the size of the label to fit the words
                    QApplication.processEvents()
                if index >= 0: # if found then call relevanat function
                    self.label2.setText(self.label2.text() + translationArray[1][index] + ", ") # concaitnate label with morse
                    self.label2.adjustSize() # update the size of the label to fit the words
                    QApplication.processEvents()
                    for x in translationArray[1][index]:
                        #print(x)
                        if x == '-':                        
                            Da()
                            sleep(morseTimeUnit)
                        else:
                            Dit()
                            sleep(morseTimeUnit)
                    CharGap()
                else:
                    self.label2.setText("ERROR: Invalid Character found") # change value in label
                    self.label2.adjustSize() # update the size of the label to fit the words
                    QApplication.processEvents()                                    

def window():
    app = QApplication(sys.argv) #setup OS based application       
    win = MyWindow() # create window 
    win.show() # show the window, must be after changes
    sys.exit(app.exec()) # clean window exit, must be last

window() # call window func
GPIO.cleanup()
print("Clean complete.")
