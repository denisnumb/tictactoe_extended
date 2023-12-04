import json
from typing import List
from enum import Enum


x = '❌'
o = '⭕'
TIE = 'T'

class ButtonStyleType(int, Enum):
    DEFAULT = 0
    X_WIN = 1
    O_WIN = 2
    X_HOVER = 3
    O_HOVER = 4

class Player:
	def __init__(self, name: str, *, is_bot: bool=False, is_client_socket: bool=False):
		self.name = name
		self.is_bot = is_bot
		self.is_client_socket = is_client_socket

class ButtonState:
    def __init__(self, name: str, symbol: str, styles: List[int | ButtonStyleType], is_enabled: bool):
        self.name = name
        self.symbol = symbol
        self.styles = [ButtonStyleType(style) for style in styles]
        self.is_enabled = is_enabled

class SocketServerData:
    def __init__(self, message: str, button_states: List[ButtonState]):
        self.message = message
        self.button_states = button_states

    def get_json(self) -> str:
        data = self.__dict__
        data['button_states'] = [state.__dict__ for state in self.button_states]
        return json.dumps(data, ensure_ascii=False)

class SocketClientDataType:
    USERNAME = 0
    BUTTON = 1

class SocketClientData:
    def __init__(self, type: int, content: str):
        self.type = type
        self.content = content

    def get_json(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)