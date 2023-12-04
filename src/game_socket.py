import json
import socket
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from model import (
	SocketServerData,
	SocketClientData,
	SocketClientDataType,
	ButtonState
)


class BaseSocket:
	def receive_data(self, sender: socket.socket) -> str:
		l = int.from_bytes(self.receive_part(sender, 2), "big")
		return self.receive_part(sender, l).decode('utf-8')

	def receive_part(self, sender: socket.socket, to_receive: int) -> bytes:
		received = b''
		while len(received) < to_receive:
			chunk = sender.recv(min(to_receive - len(received), 2048))
			if chunk == b'':
				raise RuntimeError('Connection lost')
			received += chunk
		return received

	def send(self, receiver: socket.socket, data: str) -> None:
		data = bytes(data, 'utf-8')
		receiver.send(len(data).to_bytes(2, 'big'))
		receiver.send(data)

class Server(BaseSocket, QThread):
	on_request = QtCore.pyqtSignal(SocketClientData)
	on_client = QtCore.pyqtSignal(SocketClientData)
	on_close = QtCore.pyqtSignal()

	def __init__(self, port: int):
		QThread.__init__(self)
		self.port = port
		self.client_connected = False
		self.keep_alive = True

	def run(self) -> None:
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.bind(('', self.port))
			self.wait_client()
		except Exception as e:
			self.stop()
			print(e)

	def stop(self) -> None:
		self.keep_alive = False
		self.close_connection()
		print('Server closed')

	def close_connection(self, exception: Exception | str='Connection closed') -> None:
		if self.client_connected:
			print(f'Client disconnected: {exception}')
			self.client.close()
			self.client_connected = False
			
			if self.keep_alive:
				self.wait_client()

		if not self.keep_alive:
			self.sock.close()
			self.on_close.emit()

	def wait_client(self) -> None:
		try:
			self.sock.listen(1)
			print('Waiting for client...')
			self.client, address = self.sock.accept()
			print(f'Client connected: [{address[0]}:{address[1]}]')
			self.client_connected = True
			self.on_client.emit(SocketClientData(**json.loads(self.receive_data(self.client))))
			self.receive_button()
		except:
			pass

	def send_game_data(self, data: SocketServerData) -> None:
		if not self.client_connected:
			return
		try:
			self.send(self.client, data.get_json())
		except Exception as e:
			self.close_connection(e)

	def receive_button(self) -> None:
		try:
			while self.keep_alive:
				self.on_request.emit(SocketClientData(**json.loads(self.receive_data(self.client))))
		except Exception as e:
			self.close_connection(e)

class Client(BaseSocket, QThread):
	on_request = QtCore.pyqtSignal(SocketServerData)
	on_disconnected = QtCore.pyqtSignal()
	on_connected = QtCore.pyqtSignal()

	def __init__(self, ip: str, port: int, name: str):
		QThread.__init__(self)
		self.ip = ip
		self.port = port
		self.name = name
		self.connected = False

	def run(self) -> None:
		self.connected = self.try_connect()
		if self.connected:
			self.on_connected.emit()
			self.receive_game_data()
		else:
			self.close_connection()

	def try_connect(self) -> bool:
		if self.connected:
			return
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print(f'Connecting to {self.ip}:{self.port}...')
			self.sock.connect((self.ip, self.port))
			print(f'Connected to server [{self.ip}:{self.port}]')
			self.send(self.sock, SocketClientData(SocketClientDataType.USERNAME, self.name).get_json())
			return True
		except:
			print('Connection failed')
			return False

	def close_connection(self, exception: Exception | str='Connection closed') -> None:
		if self.connected:
			print(f'Connection lost: {exception}')
			self.sock.close()
			self.connected = False
		self.on_disconnected.emit()

	def send_button(self, button_name: str) -> None:
		if not self.connected:
			return
		try:
			self.send(self.sock, SocketClientData(SocketClientDataType.BUTTON, button_name).get_json())
		except Exception as e:
			self.close_connection(e)

	def receive_game_data(self) -> None:
		try:
			while True:
				raw_data = json.loads(self.receive_data(self.sock))
				self.on_request.emit(SocketServerData(
					message=raw_data['message'],
					button_states=[
						ButtonState(**state) 
						for state in raw_data['button_states']
					]
				))
		except Exception as e:
			self.close_connection(e)