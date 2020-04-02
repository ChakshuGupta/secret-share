import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from shamir39.shamir_shares import generate, split_shares, combine_shares

qtCreatorFile = "app_ui.ui"
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class SecretShareApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.generateButton.clicked.connect(self.generate_mnemonics)
        self.splitButton.clicked.connect(self.split_key)
        self.exportButton.clicked.connect(self.export_shares)
        self.combineButton.clicked.connect(self.recover_key)

    def generate_mnemonics(self):
        """
        Callback function for generate button
        """
        number_of_words = int(self.numberWords.currentText())
        mnemonics = generate(number_of_words)

        self.sharesTextEdit.clear()
        self.mnemonicsTextEdit.setText(mnemonics)

    def split_key(self):
        """
        Callback function for split button
        """
        m = self.mBox.value()
        n = self.nBox.value()
        mnemonics = self.mnemonicsTextEdit.toPlainText()
        shares = split_shares(mnemonics, m, n)
        shares_text = "\n\n".join(shares)

        self.sharesTextEdit.setText(shares_text)

    def export_shares(self):
        """
        Callback function for export button
        """
        shares = self.sharesTextEdit.toPlainText().split("\n\n")

        if self.singleRadioButton.isChecked():
            file_handler = open("shamir-share.txt", "w")
            for share in shares:
                file_handler.write(share)
                file_handler.write("\n")
            file_handler.close()

        if self.multiRadioButton.isChecked():
            for share in shares:
                file_handler = open("shamir-share-{}.txt".format(shares.index(share)+1), "w")
                file_handler.write(share)
                file_handler.close()

    
    def recover_key(self):
        """
        Callback function for combine button to recover the key
        """
        input_shares = self.recoverSharesTextEdit.toPlainText().split("\n")
        shares = list()
        for share in input_shares:
            share = share.strip()
            if share != "":
                shares.append(share)
        print(input_shares)            
        recovered_key = combine_shares(shares)
        self.recoveredKeyTextEdit.setText(recovered_key)

 
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SecretShareApp()
    window.show()
    sys.exit(app.exec_())