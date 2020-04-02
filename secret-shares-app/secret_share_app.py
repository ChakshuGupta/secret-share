import sys
import json

from PyQt5 import QtCore, QtPrintSupport, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from shamir39.shamir_shares import generate, split_shares, combine_shares, Encoding
from werkzeug.exceptions import BadRequest

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
        self.resetSplitButton.clicked.connect(self.reset_split)
        self.resetCombineButton.clicked.connect(self.reset_combine)
        self.printButton.clicked.connect(self.print_document)


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
        try:
            m = self.mBox.value()
            n = self.nBox.value()
            mnemonics = self.mnemonicsTextEdit.toPlainText()
            encoding = Encoding.BIP39
            if self.encodingComboBox1.currentIndex() == 1:
                encoding = Encoding.BASE58

            shares = split_shares(mnemonics, m, n, encoding)
            shares_text = "\n\n".join(shares)

            self.sharesTextEdit.setText(shares_text)
        
        except BadRequest as e:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage("Bad Request! Invalid Input!")
        
        except Exception:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage("Error!")


    def export_shares(self):
        """
        Callback function for export button
        """
        shares = self.sharesTextEdit.toPlainText().split("\n\n")

        try:
            if self.singleRadioButton.isChecked():
                file_handler = open("shamir-share.txt", "w")
                for share in shares:
                    file_handler.write(share)
                    file_handler.write("\n")
                file_handler.close()
                QMessageBox.about(self, "Success" , "Shares export to text file succeeded!")

            else:
                for share in shares:
                    file_handler = open("shamir-share-{}.txt".format(shares.index(share)+1), "w")
                    file_handler.write(share)
                    file_handler.close()
                QMessageBox.about(self, "Success" , "Shares export to separate files succeeded!")

        except IOError as e:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage("Error exporting shares to file!")

        except Exception:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage("Error!")

    
    def recover_key(self):
        """
        Callback function for combine button to recover the key
        """
        try:
            input_shares = self.recoverSharesTextEdit.toPlainText().split("\n")
            encoding = Encoding.BIP39
            if self.encodingComboBox2.currentIndex() == 1:
                encoding = Encoding.BASE58

            shares = list()
            for share in input_shares:
                share = share.strip()
                if share != "":
                    shares.append(share)          
            recovered_key = combine_shares(shares, encoding)
            self.recoveredKeyTextEdit.setText(recovered_key)
        
        except BadRequest as e:
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.showMessage("Bad Request! Invalid input!")
        
        except Exception:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage("Error!")


    def reset_split(self):
        """
        Callback function for the reset in split tab
        """
        self.sharesTextEdit.clear()
        self.mnemonicsTextEdit.clear()
        self.singleRadioButton.setChecked(True)
        self.encodingComboBox1.setCurrentIndex(0)


    def reset_combine(self):
        """
        Callback function for the reset in combine tab
        """
        self.recoverSharesTextEdit.clear()
        self.recoveredKeyTextEdit.clear()
        self.encodingComboBox2.setCurrentIndex(0)


    
    def print_document(self):
        """
        Callback function for the print button
        """

        shares = self.sharesTextEdit.toPlainText().split("\n\n")
        if len(shares) > 0:
            if self.singleRadioButton.isChecked():
                dialog = QtPrintSupport.QPrintDialog()
                if dialog.exec_() == QtWidgets.QDialog.Accepted:
                    self.sharesTextEdit.document().print_(dialog.printer())
            
            else:
                for share in shares:
                    dialog = QtPrintSupport.QPrintDialog()
                    if dialog.exec_() == QtWidgets.QDialog.Accepted:
                        print_doc = QTextDocument(share)
                        print_doc.print_(dialog.printer())
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage("No shares entered!")

                

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SecretShareApp()
    window.show()
    sys.exit(app.exec_())