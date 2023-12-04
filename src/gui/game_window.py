import os
from random import choice
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget
from ui.ui_game_window import UiGameWindow
from tic_tac_toe import TicTacToeExtended
from model import Player, SocketServerData, SocketClientData
from game_socket import Server, Client
from utils import set_button_icon, set_button_style


class GameWindow(QWidget):
	on_close = QtCore.pyqtSignal()

	def __init__(self, x_position: int, y_position: int):
		QWidget.__init__(self, None)
		self.ui = UiGameWindow()
		self.ui.setupUi(self)
		self.move(x_position, y_position)

	def closeEvent(self, _) -> None:
		self.close()
		self.on_close.emit()

	def play_with_bot(self) -> None:
		game = TicTacToeExtended(
			self, 
			self.ui.buttons, 
			Player(os.getlogin()), 
			Player('Bot', is_bot=True)
		)
		game.start_game(zero_first=choice((True, False)))

	def play_with_player(self) -> None:
		game = TicTacToeExtended(
			self, 
			self.ui.buttons, 
			Player(os.getlogin()),
			Player('Second'),
			time_to_move=30
		)
		game.start_game(zero_first=choice((True, False)))

	def start_server_game(self, server: Server, username: str) -> None:
		def on_client_request(data: SocketClientData) -> None:
			field_index, row, column = map(int, data.content)
			game.fields[field_index].buttons[row*3+column].callback(game.player2)

		def on_client_reconnected(data: SocketClientData):
			game.player2.name = data.content
			game.update_message()
			QTimer.singleShot(300, game.send_data_to_client)

		game = TicTacToeExtended(
			self,
			self.ui.buttons,
			Player(os.getlogin()),
			Player(username, is_client_socket=True),
			server=server
		)
		game.start_game(zero_first=False)
		QTimer.singleShot(300, game.send_data_to_client)

		server.on_request.connect(on_client_request)
		server.on_client.connect(on_client_reconnected)
		

	def start_from_client(self, client: Client) -> None:
		def on_server_request(data: SocketServerData) -> None:
			self.setWindowTitle(data.message)

			for button, state in zip(self.ui.buttons_flat, data.button_states):
				if button.objectName() == state.name:
					button.setEnabled(state.is_enabled)
					set_button_style(button, state.styles)
					if state.symbol:
						set_button_icon(button, state.symbol)


		client.on_request.connect(on_server_request)
		client.on_disconnected.connect(self.close)

		for button in self.ui.buttons_flat:
			button.setEnabled(False)
			button.clicked.connect(
				lambda _, button=button: client.send_button(button.objectName())
			)