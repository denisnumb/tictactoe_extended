from PyQt5.QtWidgets import QDialog
from ui.ui_config_game_dialog import UiConfigGameDialog
from random import choice


class ConfigGameDialog(QDialog):
	def __init__(self, x_position: int, y_position: int):
		QDialog.__init__(self, None)
		self.ui = UiConfigGameDialog()
		self.ui.setupUi(self)
		self.setFixedSize(410, 460)
		self.move(x_position + 195, y_position + 70)

		self.ui.start_button.clicked.connect(self.play)

		self.ui.time_to_move_check.stateChanged.connect(
			lambda _: self.ui.time_to_move_spin.setEnabled(self.ui.time_to_move_check.isChecked())
		)

		self.ui.o_button.toggled.connect(lambda _: self.set_zero_first(True))
		self.ui.x_button.toggled.connect(lambda _: self.set_zero_first(False))
		self.ui.random_button.toggled.connect(
			lambda _, value=choice((True, False)): self.set_zero_first(value)
		)

		self.next = False
		self.player1_name = 'Игрок 1'
		self.player2_name = 'Игрок 2'
		self.time_to_move = 0
		self.zero_first = choice((True, False))

	def set_zero_first(self, value: bool) -> None:
		self.zero_first = value

	def play(self) -> None:
		if self.ui.time_to_move_spin.isEnabled():
			self.time_to_move = self.ui.time_to_move_spin.value()
		self.player1_name = self.ui.player1_name_edit.text() or self.player1_name
		self.player2_name = self.ui.player2_name_edit.text() or self.player2_name
		self.next = True
		self.accept()