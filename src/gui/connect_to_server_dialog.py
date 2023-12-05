from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal, QRegExp, QTimer
from PyQt5.QtGui import QRegExpValidator
from ui.ui_connect_to_server_dialog import UiConnectToServerDialog
from resources.styles import default_button_style, error_button_style
import re


class ConnectToServerDialog(QDialog):
	on_connect_clicked = pyqtSignal(object)

	def __init__(self, x_position: int, y_position: int):
		QDialog.__init__(self, None)
		self.ui = UiConnectToServerDialog()
		self.ui.setupUi(self)
		self.setFixedSize(410, 250)
		self.move(x_position + 195, y_position + 175)

		self.ui.connect_button.clicked.connect(self.connect)
		self.ui.server_port_edit.textEdited.connect(self.on_port_edit)
		ipRange = '(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])' 
		self.ui.server_ip_edit.setValidator(QRegExpValidator(QRegExp('^'+ipRange+r'\.'+ipRange+r'\.'+ipRange+r'\.'+ipRange+'$'), self))

		self.player_name = 'Client'
		self.ip = ''
		self.port = 1337

	def set_connecting(self) -> None:
		self.ui.connect_button.setText('Подключение...')
		self.ui.connect_button.setEnabled(False)

	def on_connectiong_error(self) -> None:
		self.ui.connect_button.setStyleSheet(error_button_style)
		self.ui.connect_button.setText('Не удалось подключиться')
		QTimer.singleShot(1000, self.__reset_connect_button)
		
	def __reset_connect_button(self) -> None:
		self.ui.connect_button.setStyleSheet(default_button_style)
		self.ui.connect_button.setText('Подключиться')
		self.ui.connect_button.setEnabled(True)

	def on_port_edit(self) -> None:
		self.ui.server_port_edit.setText(
			re.sub('\D', '', self.ui.server_port_edit.text())
		)

	def connect(self) -> None:
		self.player_name = self.ui.player_name_edit.text() or self.player_name
		self.port = int(self.ui.server_port_edit.text())
		self.ip = self.ui.server_ip_edit.text() or '127.0.0.1'
		self.on_connect_clicked.emit(self)