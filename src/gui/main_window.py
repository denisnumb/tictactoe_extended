from PyQt5.QtWidgets import QMainWindow, QInputDialog
from ui.ui_main_window import UiMainWindow
from gui.game_window import GameWindow
from gui.config_game_dialog import ConfigGameDialog
from gui.server_start_dialog import ServerStartDialog
from gui.play_online_dialog import PlayOnlineDialog
from gui.connect_to_server_dialog import ConnectToServerDialog
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
		game = GameWindow(self.x(), self.y())
		game.on_close.connect(self.show)
		return game

	def play_with_bot(self) -> None:
		game = self.prepare_game_window()
		self.hide()
		game.play_with_bot()
		game.show()

	def play_with_player(self) -> None:
		cfg = ConfigGameDialog(self.x(), self.y())
		cfg.exec()

		if cfg.next:
			game = self.prepare_game_window()
			self.hide()
			game.play_with_player(cfg.player1_name, cfg.player2_name, cfg.time_to_move, cfg.zero_first)
			game.show()

	def play_online(self) -> None:
		mode_dialog = PlayOnlineDialog(self.x(), self.y())
		mode_dialog.exec()

		if mode_dialog.next:
			if mode_dialog.start_server:
				start_server_dialog = ServerStartDialog(self.x(), self.y())
				start_server_dialog.on_server_start.connect(self.run_server)
				start_server_dialog.exec()

			if mode_dialog.connect:
				connect_dialog = ConnectToServerDialog(self.x(), self.y())
				connect_dialog.on_connect_clicked.connect(self.run_client)
				connect_dialog.exec()


	def run_server(self, dialog: ServerStartDialog) -> None:
		if self.server:
			return

		def on_close():
			dialog.on_start_server_error()
			self.server = None

		def on_client(data: SocketClientData):
			dialog.accept()
			self.server.on_client.disconnect(on_client)
			self.hide()
			game = self.prepare_game_window()
			game.on_close.connect(self.server.stop)
			game.start_server_game(self.server, dialog.player_name, data.content, dialog.time_to_move, dialog.zero_first)
			game.show()

		dialog.set_client_waiting()
		self.server = Server(dialog.port)
		self.server.on_client.connect(on_client)
		self.server.on_close.connect(on_close)
		dialog.on_close.connect(self.server.stop)
		self.server.start()


	def run_client(self, dialog: ConnectToServerDialog) -> None:
		if self.client:
			return

		def on_disconnected():
			dialog.on_connectiong_error()
			self.client.disconnect()
			self.client = None

		def on_connect():
			dialog.accept()
			self.hide()
			game = self.prepare_game_window()
			game.on_close.connect(self.client.close_connection)
			game.start_from_client(self.client)
			game.show()
		
		dialog.set_connecting()
		self.client = Client(dialog.ip, dialog.port, dialog.player_name)
		self.client.on_connected.connect(on_connect)
		self.client.on_disconnected.connect(on_disconnected)
		self.client.start()
		