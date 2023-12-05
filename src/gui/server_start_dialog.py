from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal, QTimer
from ui.ui_start_server_dialog import UiServerStartDialog
from resources.styles import default_button_style, error_button_style
from random import choice
import re


class ServerStartDialog(QDialog):
	on_close = pyqtSignal()
	on_server_start = pyqtSignal(object)

	def __init__(self, x_position: int, y_position: int):
		QDialog.__init__(self, None)
		self.ui = UiServerStartDialog()
		self.ui.setupUi(self)
		self.setFixedSize(410, 460)
		self.move(x_position + 195, y_position + 70)

		self.ui.start_button.clicked.connect(self.start_server)

		self.ui.time_to_move_check.stateChanged.connect(
			lambda _: self.ui.time_to_move_spin.setEnabled(self.ui.time_to_move_check.isChecked())
		)

		self.ui.o_button.toggled.connect(lambda _: self.set_zero_first(True))
		self.ui.x_button.toggled.connect(lambda _: self.set_zero_first(False))
		self.ui.random_button.toggled.connect(
			lambda _, value=choice((True, False)): self.set_zero_first(value)
		)

		self.ui.server_port_edit.textEdited.connect(self.on_port_edit)

		self.player_name = 'Host'
		self.time_to_move = 0
		self.port = 1337
		self.zero_first = choice((True, False))

	def closeEvent(self, _) -> None:
		self.close()
		self.on_close.emit()

	def on_port_edit(self) -> None:
		self.ui.server_port_edit.setText(
			re.sub('\D', '', self.ui.server_port_edit.text())
		)

	def set_zero_first(self, value: bool) -> None:
		self.zero_first = value

	def set_client_waiting(self) -> None:
		self.ui.start_button.setText('Ожидание игрока...')
		for element in self.findChildren(QWidget):
			element.setEnabled(False)

	def on_start_server_error(self) -> None:
		self.ui.start_button.setStyleSheet(error_button_style)
		self.ui.start_button.setText('Не удалось запустить сервер')
		QTimer.singleShot(1000, self.__reset_elements)
		
	def __reset_elements(self) -> None:
		self.ui.start_button.setStyleSheet(default_button_style)
		self.ui.start_button.setText('Запустить сервер')
		for element in self.findChildren(QWidget):
			element.setEnabled(True)

		self.ui.time_to_move_spin.setEnabled(self.ui.time_to_move_check.isChecked())

	def start_server(self) -> None:
		if self.ui.time_to_move_spin.isEnabled():
			self.time_to_move = self.ui.time_to_move_spin.value()
		self.player_name = self.ui.player_name_edit.text() or self.player_name
		self.port = int(self.ui.server_port_edit.text())
		self.on_server_start.emit(self)