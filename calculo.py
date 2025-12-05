import sys
import shutil
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QSizePolicy
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

RUBY_SCRIPT = 'calculator.rb'

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculo')
        self.setFixedSize(360, 480)

        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(60)
        
        self.display.setStyleSheet("""
        QWidget {
            background-color: #53629E; 
            color: white;          
                                   border-radius: 5px;
                                   font-size: 45px;
        }
        QPushButton {
            background-color: #4c566a;
            border: none;
        }         
        """)
        

        self.op1 = None
        self.op = None
        self.tunggu2 = False

        layout = QGridLayout()
        layout.addWidget(self.display, 0, 0, 1, 4)

        buttons = [
            ('7', self.digit), ('8', self.digit), ('9', self.digit), ('/', self.operator),
            ('4', self.digit), ('5', self.digit), ('6', self.digit), ('x', self.operator),
            ('1', self.digit), ('2', self.digit), ('3', self.digit), ('-', self.operator),
            ('0', self.digit), ('.', self.dot),  ('^', self.operator), ('+', self.operator),
            ('C', self.clear), ('%', self.operator), ('=', self.equals),
        ]

        positions = [(i+1, j) for i in range(5) for j in range(4)]
        # add only as many positions as buttons
        for position, (text, handler) in zip(positions, buttons):
            btn = QPushButton(text)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.clicked.connect(lambda checked, t=text, h=handler: h(t))
            layout.addWidget(btn, *position)

        self.setLayout(layout)

    def digit(self, ch):
        if self.display.text() == '0' or (self.tunggu2 and self.op is not None):
            self.display.setText(ch)
            self.tunggu2 = False
        else:
            self.display.setText(self.display.text() + ch)

    def dot(self, ch):
        if '.' not in self.display.text():
            self.display.setText(self.display.text() + '.')

    def operator(self, opch):
        try:
            self.op1 = float(self.display.text())
        except ValueError:
            self.display.setText('Error')
            return
        self.op = opch
        self.tunggu2 = True

    def clear(self, _=None):
        self.display.setText('0')
        self.op1 = None
        self.op = None
        self.tunggu2 = False

    def equals(self, _=None):
        if self.op is None or self.op1 is None:
            return
        try:
            op2 = float(self.display.text())
        except ValueError:
            self.display.setText('Error')
            return

        # cek keberadaan interpreter ruby dan script
        if shutil.which('ruby') is None:
            self.display.setText('Ruby not found')
            return

        # panggil calculator.rb dengan tiga argumen: operator op1 op2
        try:
            # Gunakan list args untuk mencegah injection shell
            proc = subprocess.run(
                ['ruby', RUBY_SCRIPT, self.op, str(self.op1), str(op2)],
                capture_output=True,
                text=True,
                check=False,
                timeout=5.0
            )
        except Exception as e:
            self.display.setText('Err')
            return

        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()

        if proc.returncode != 0:
            # Ruby script melaporkan error
            if stderr:
                self.display.setText('Err: ' + stderr)
            else:
                self.display.setText('Err')
            return

        # tampilkan hasil dari stdout
        self.display.setText(stdout)
        # reset state
        self.op1 = None
        self.op = None
        self.tunggu2 = False
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("logo.png"))
    app.setStyleSheet("""
                      QWidget {    
                        background-color: #473472;
                        color: white;
                        font-size: 20px;
                      }
                      QIcon {
                        border-radius: 2px;
                      }
                      QPushButton {
                        background-color: #53629E;
                        border: 2px solid black;
                        border-radius: 10px;
                        padding: 10px;
                        font-size: 20px;    
                      }
                      QPushButton:hover {
                        background-color: #87BAC3;
                      }
                      QPushButton:pressed {
                        background-color: black;
                      }
                      QLineEdit {
                        background-color: #1e1e1e;
                        border: 2px solid #D6F4ED;
                        border-radius: 8px;
                        padding: 5px;
                        font-size: 20px;
                      }
                """)
    w = Calculator()
    w.show()
    sys.exit(app.exec_())
