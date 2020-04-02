import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from shamir39.shamir_shares import generate, split_shares

qtCreatorFile = "app_ui.ui"
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class SecretShareApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.generateButton.clicked.connect(self.generate_mnemonics)
        self.splitButton.clicked.connect(self.split_key)

    def generate_mnemonics(self):
        number_of_words = int(self.numberWords.currentText())
        mnemonics = generate(number_of_words)

        self.sharesTextEdit.clear()
        self.mnemonicsTextEdit.setText(mnemonics)

    def split_key(self):
        m = self.mBox.value()
        n = self.nBox.value()
        mnemonics = self.mnemonicsTextEdit.toPlainText()
        shares = split_shares(mnemonics, m, n)
        shares_text = "\n\n".join(shares)

        self.sharesTextEdit.setText(shares_text)
 
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SecretShareApp()
    window.show()
    sys.exit(app.exec_())