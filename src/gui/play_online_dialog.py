from PyQt5.QtWidgets import QDialog
from ui.ui_play_online_dialog import UiPlayOnlineDialog


class PlayOnlineDialog(QDialog):
	def __init__(self, x_position: int, y_position: int):
		QDialog.__init__(self, None)
		self.ui = UiPlayOnlineDialog()
		self.ui.setupUi(self)
		self.setFixedSize(410, 155)
		self.move(x_position + 195, y_position + 222)

		self.ui.start_server_button.clicked.connect(self.on_start_server_select)
		self.ui.connect_button.clicked.connect(self.on_connect_select)

		self.next = False
		self.start_server = False
		self.connect = False
		
	def on_start_server_select(self) -> None:
		self.next = True
		self.start_server = True
		self.accept()

	def on_connect_select(self) -> None:
		self.next = True
		self.connect = True
		self.accept()