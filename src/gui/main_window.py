from PyQt5.QtWidgets import QMainWindow, QInputDialog
from ui.ui_main_window import UiMainWindow
from gui.game_window import GameWindow
from game_socket import Server, Client
from model import SocketClientData


class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self, None)
		self.ui = UiMainWindow()
		self.ui.setupUi(self)
		self.setFixedSize(800, 600)

		self.ui.play_with_bot_button.clicked.connect(self.play_with_bot)
		self.ui.play_with_player_button.clicked.connect(self.play_with_player)
		self.ui.play_online_button.clicked.connect(self.play_online)

		self.server: Server = None
		self.client: Client = None

	def prepare_game_window(self) -> GameWindow:
		game = GameWindow(self.pos().x(), self.pos().y())
		game.on_close.connect(self.show)
		return game

	def play_with_bot(self) -> None:
		game = self.prepare_game_window()
		self.hide()
		game.play_with_bot()
		game.show()

	def play_with_player(self) -> None:
		game = self.prepare_game_window()
		self.hide()
		game.play_with_player()
		game.show()

	def play_online(self) -> None:
		text, next = QInputDialog.getText(self, 'Input Dialog', '1) Server, 2) Client')

		if not next:
			return

		if text == '1':
			return self.run_server()

		ip, next1 = QInputDialog.getText(self, 'Input Dialog', 'ВВЕДИ АЙПИ')
		username, next2 = QInputDialog.getText(self, 'Input Dialog', 'Enter name')

		if next1 and next2:
			self.run_client(ip or '127.0.0.1', username)

	def run_server(self) -> None:
		if self.server:
			return

		def on_close():
			self.server = None

		def on_client(data: SocketClientData):
			self.server.on_client.disconnect(on_client)
			self.hide()
			game.start_server_game(self.server, data.content)
			game.show()

		game = self.prepare_game_window()
		self.server = Server(1337)
		self.server.on_client.connect(on_client)
		self.server.on_close.connect(on_close)
		game.on_close.connect(self.server.stop)
		self.server.start()


	def run_client(self, ip: str, username: str) -> None:
		if self.client:
			return

		def on_disconnected():
			self.client.disconnect()
			self.client = None

		def on_connect():
			self.hide()
			game.start_from_client(self.client)
			game.show()
		
		game = self.prepare_game_window()
		self.client = Client(ip, 1337, username)
		self.client.on_connected.connect(on_connect)
		self.client.on_disconnected.connect(on_disconnected)
		game.on_close.connect(self.client.close_connection)
		self.client.start()
		