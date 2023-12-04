import sys
sys.dont_write_bytecode = True

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from resources.styles import main_style, default_button_style
from resources import image_data

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(':icon.ico'))
app.setStyleSheet(main_style + default_button_style) 
main_style = MainWindow()
main_style.show()
sys.exit(app.exec_())