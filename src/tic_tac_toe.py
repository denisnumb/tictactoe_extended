from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QPushButton, QDialog
from random import randint, choice
from typing import List, Union, Tuple
from game_socket import Server
from utils import (
	set_button_icon, 
	set_ttt_button_style,
	win_button_styles,
	hover_button_styles
)
from model import (
	x, 
	o, 
	TIE, 
	Player, 
	SocketServerData, 
	ButtonState,
	ButtonStyleType
)


class TTTGameStates:
	CONTINUE = 0
	HAS_WINNER = 1
	TIE = 2

class TicTacToeStatic:
	line_indexes = (
		(0, 1, 2), (3, 4, 5), (6, 7, 8),
		(0, 3, 6), (1, 4, 7), (2, 5, 8),
		(0, 4, 8), (6, 4, 2)
	)

	@staticmethod
	def get_field_free_indexes(field: List[str]) -> List[int]:
		return [x for x in range(len(field)) if not field[x]]

	@staticmethod
	def check_winner(field: List[str]) -> Tuple[Union[None, str], int]:
		tie = ('❌❌⭕', '❌⭕⭕', '❌⭕❌', '⭕❌⭕', '⭕⭕❌', '⭕❌❌')
		all_lines = TicTacToeStatic.get_lines(field)

		tie_lines = 0
		for line in all_lines:
			if line in ('❌❌❌', '⭕⭕⭕'):
				return x if line == '❌❌❌' else o, TTTGameStates.HAS_WINNER
			if line in tie or TIE in line:
				tie_lines += 1

		return None, TTTGameStates.TIE if tie_lines == len(all_lines) else TTTGameStates.CONTINUE 

	@staticmethod
	def get_lines(field: List[str]) -> List[str]:
		return [''.join(map(lambda i: ' ' if not field[i] else field[i], indexes)) for indexes in TicTacToeStatic.line_indexes]


class TicTacToeButton:
	def __init__(self, game, button: QPushButton, index: int):
		self.game: TicTacToe = game
		self.button = button
		self.index = index
		self.style = ButtonStyleType.DEFAULT
		self.hover_style = hover_button_styles[self.game.current_symbol]
		self.button.clicked.connect(lambda _: self.callback(
			self.game.player1 
			if self.game.player2.is_bot or self.game.player2.is_client_socket
			else self.game.current_player
		))
		
	def callback(self, player: Player) -> None:	
		game: 'TicTacToe' = self.game
		
		if player != game.current_player or game.field[self.index] in (x, o):
			return

		if not game.parent_game.current_field:
			game.parent_game.current_field = game

		self.__set_state_used()

		if game_state := game.update_state():
			game.stop_game(game_state)
	
		if game_state := game.parent_game.update_state():
			return game.parent_game.stop_game(game_state)

		game.parent_game.current_field = game.parent_game.fields[self.index]
		game.parent_game.check_next_move()

	def __set_state_used(self) -> None:
		set_ttt_button_style(self, style=win_button_styles[self.game.current_symbol])
		set_button_icon(self.button, self.game.current_symbol)
		self.game.field[self.index] = self.game.current_symbol
		self.game.switch_current_player()
		self.game.parent_game.reset_move_time()

class TicTacToe:
	@property
	def current_symbol(self) -> str:
		return self.parent_game.current_symbol

	@current_symbol.setter
	def current_symbol(self, symbol: str) -> None:
		self.parent_game.current_symbol = symbol

	@property
	def player1(self) -> Player:
		return self.parent_game.player1

	@property
	def player2(self) -> Player:
		return self.parent_game.player2

	@property
	def current_player(self) -> Player:
		return self.player1 if self.current_symbol == x else self.player2

	def __init__(self, parent_game: 'TicTacToeExtended', index: int, buttons: List[QPushButton]):
		self.parent_game: 'TicTacToeExtended' = parent_game
		self.buttons: List[TicTacToeButton] = []
		self.index = index
		self.winner_symbol= ''
		self.game_over = False
		self.game_state = TTTGameStates.CONTINUE

		self.field = ['']*9

		for i, button in enumerate(buttons):
			self.buttons.append(TicTacToeButton(self, button, i))

	def switch_current_player(self) -> None:
		self.current_symbol = o if self.current_symbol == x else x

	def disable_all_buttons(self, *, set_winner_style: bool=False) -> None:
		for ttt_button in self.buttons:
			ttt_button.button.setEnabled(False)

		if set_winner_style:
			for ttt_button in self.buttons:
				set_ttt_button_style(ttt_button, style=win_button_styles[self.winner_symbol])

	def enable_all_buttons(self) -> None:
		for ttt_button in self.buttons:
			ttt_button.button.setEnabled(True)

	def stop_game(self, state: int) -> None:
		self.disable_all_buttons(set_winner_style=bool(self.winner_symbol))
		self.parent_game.field[self.index] = self.winner_symbol or TIE
		self.game_state = state
		self.game_over = True

	def bot_move(self) -> None:
		free_indexes = TicTacToeStatic.get_field_free_indexes(self.field)
		all_lines = TicTacToeStatic.get_lines(self.field)

		def choice_if_availible(indexes: List[int]) -> int:
			if free := [index for index in indexes if index in free_indexes]:
				return choice(free)
			return choice(free_indexes)

		# первый ход бота будет осмысленным, помешать возможности победить, осмысленный ход, бот будет мешать
		chances = (50, 95, 80, 40)

		max_zero_count_index = 0
		max_zero_count = 0
		max_x_count_index = 0
		max_x_count = 0

		# проходим по 6 строкам и 2 диагоналям
		for i, line in enumerate(all_lines):
			# если в них есть пустые клетки
			if ' ' in line:
				# запоминаем строку, в которой больше всего крестиков
				if (x_count := line.count('❌')) > max_x_count:
					max_x_count_index = i
					max_x_count = x_count
				# запоминаем строку, в которой больше всего ноликов и при этом как можно меньше крестиков
				o_count = line.count('⭕')
				if o_count > max_zero_count or (o_count == max_zero_count and x_count < max_x_count):
					max_zero_count_index = i
					max_zero_count = o_count

		# если это первый ход бота (ноликов еще нет)
		if not self.field.count(o):
			# если игрок сходил в угол, то с шансом в chances[0]% бот будет блокировать эту схему ходом в боковую и центральную клетки
			chance = randint(1, 100)
			if any([index not in free_indexes for index in (0, 2, 6, 8)]) and chance <= chances[0]:
				return self.make_move(choice_if_availible((3, 1, 7, 5, 4)))
			elif chance <= chances[0]:
				# иначе делает ход в угол или центр
				return self.make_move(choice_if_availible((0, 2, 6, 8, 4)))
			
		# если в какой-то линии крестиков уже 2 и все еще нет линии, где есть 2 нолика
		# то нужно защищаться, блокируя клетки с крестиками
		elif max_x_count > 1 and max_zero_count < 2:
			# шанс на правильный ход chances[1]%
			if randint(1, 100) <= chances[1]:
				for i, cell in zip(TicTacToeStatic.line_indexes[max_x_count_index], all_lines[max_x_count_index]):
					if cell != x:
						return self.make_move(i)

		# иначе, с шансом в chances[2]% бот делает осмысленный ход
		if randint(1, 100) <= chances[2]:
			# защита от крестиков в углах
			if any([index not in free_indexes for index in (0, 2, 6, 8)]) and max_zero_count < 2 and randint(1, 100) <= chances[3]:
				return self.make_move(choice_if_availible((3, 1, 7, 5, 4)))
			# ходим в любую доступную клетку из линии, где больше всего ноликов
			return self.make_move(choice([TicTacToeStatic.line_indexes[max_zero_count_index][i] for i in range(3) if all_lines[max_zero_count_index][i] == ' ']))

		return self.make_move(choice(free_indexes))
			
		
	def make_move(self, index: int) -> None:
		self.buttons[index].callback(self.current_player)

	def update_state(self) -> int:
		winner_symbol, state = TicTacToeStatic.check_winner(self.field)
		if state == TTTGameStates.HAS_WINNER:
			self.winner_symbol = winner_symbol
			
		return state

class TicTacToeExtended:
	@property
	def current_player(self) -> Player:
		return self.player1 if self.current_symbol == x else self.player2

	@property
	def current_field(self) -> TicTacToe:
		return self.__current_field

	@current_field.setter
	def current_field(self, field: TicTacToe) -> None:
		if field.game_over:
			self.playable_fields = self.find_playable_neighbours(field.index)
		else:
			self.playable_fields = [field]

		self.__current_field = self.playable_fields[0] if len(self.playable_fields) == 1 else None

		for other_field in self.fields:
			if other_field not in self.playable_fields:
				other_field.disable_all_buttons()

		for playable_field in self.playable_fields:
			playable_field.enable_all_buttons()

		self.send_data_to_client()

	@property
	def move_time(self) -> int:
		return self.__move_time

	@move_time.setter
	def move_time(self, new_value: int) -> None:
		self.__move_time = new_value
		self.update_message()

		if self.move_time == 0:
			self.current_symbol = o if self.current_symbol == x else x
			self.reset_move_time()
			self.check_next_move()

	@property
	def current_symbol(self) -> str:
		return self.__current_symbol

	@current_symbol.setter
	def current_symbol(self, new_symbol: str) -> None:
		self.__current_symbol = new_symbol

		for ttt_button in self.ttt_buttons:
			set_ttt_button_style(ttt_button, hover_style=hover_button_styles[self.current_symbol])

	def __init__(
		self, 
		window: QDialog, 
		buttons: List[List[QPushButton]], 
		player1: Player, 
		player2: Player,
		*,
		time_to_move: int=0,
		server: Server=None
		):
		self.__current_field: TicTacToe = None
		self.__current_symbol = x
		self._server = server
		self._window = window
		self.fields: List[TicTacToe] = []
		self.player1 = player1
		self.player2 = player2
		self.winner: Player = None
		self.game_over = False
		self.game_state = TTTGameStates.CONTINUE

		self.field = ['']*9

		for index, game_buttons in enumerate(buttons):
			self.fields.append(TicTacToe(self, index, game_buttons))

		self.playable_fields: List[TicTacToe] = self.fields
		self.ttt_buttons = [ttt_button for field in self.fields for ttt_button in field.buttons]

		self.__time_to_move = time_to_move
		if self.__time_to_move:
			self.__move_timer = QTimer()
			self.__move_timer.setInterval(1000)
			self.__move_timer.timeout.connect(self.update_move_time)
			self.__move_time = time_to_move

	def start_game(self, *, zero_first: bool) -> None:
		self.current_symbol = o if zero_first else x
		self.switch_move_timer()
		self.check_next_move()

	def stop_game(self, state: int) -> None:
		self.disable_all_fields()
		self.game_state = state
		self.game_over = True
		self.update_message()
		self.switch_move_timer()

	def switch_move_timer(self) -> None:
		if self.__time_to_move:
			if self.__move_timer.isActive():
				self.__move_timer.stop()
			else:
				self.__move_timer.start()

	def reset_move_time(self) -> None:
		if self.__time_to_move:
			self.move_time = self.__time_to_move

	def update_move_time(self) -> None:
		self.move_time -= 1

	def update_message(self):
		self._window.setWindowTitle(self.get_message())
		self.send_data_to_client()

	def send_data_to_client(self) -> None:
		if not self._server:
			return

		self._server.send_game_data(SocketServerData(
			self._window.windowTitle(),
			[
				ButtonState(
					name=ttt_button.button.objectName(),
					symbol=ttt_button.game.field[ttt_button.index],
					styles=[ttt_button.style, ttt_button.hover_style],
					is_enabled=ttt_button.button.isEnabled()
				)
				for ttt_button in self.ttt_buttons
			]
		))

	def disable_all_fields(self) -> None:
		for ttt in self.fields:
			for ttt_button in ttt.buttons:
				ttt_button.button.setEnabled(False)

	def find_playable_neighbours(self, field_index: int, checked_indexes: List[int]=None) -> List[TicTacToe]:
		neighbours = {
			0: (1, 3),
			1: (0, 2, 4),
			2: (1, 5),
			3: (0, 4, 6),
			4: (1, 3, 5, 7),
			5: (2, 4, 8),
			6: (3, 7),
			7: (6, 4, 8),
			8: (7, 5)
		}

		playable_neighbours = [
			self.fields[index] 
			for index in neighbours[field_index]
			if not self.fields[index].game_over
		]

		if playable_neighbours:
			return playable_neighbours

		playable_neighbours = set()

		if not checked_indexes:
			checked_indexes = [field_index]

		for index in neighbours[field_index]:
			if index not in checked_indexes:
				checked_indexes.append(index)
				playable_neighbours.update(
					set(self.find_playable_neighbours(index, checked_indexes))
				)

		return list(playable_neighbours)

	def check_next_move(self) -> None:
		self.update_message()

		if self.current_player.is_bot:
			if not self.current_field:
				self.current_field = choice(self.playable_fields)
			return QTimer.singleShot(1000, self.current_field.bot_move)

	def update_state(self) -> int:
		winner_symbol, state = TicTacToeStatic.check_winner(self.field)
		if state == TTTGameStates.HAS_WINNER:
			self.winner = self.player1 if winner_symbol == x else self.player2
			
		return state

	def get_message(self) -> str:
		if self.game_over:
			match self.game_state:
				case TTTGameStates.HAS_WINNER:
					return f'Игра между {self.player1.name} и {self.player2.name} окончена, победил {self.winner.name}!'
				case TTTGameStates.TIE:
					return f'Игра между {self.player1.name} и {self.player2.name} окончена, ничья'

		if not self.current_player.is_bot:
			time_to_move = f' [{self.move_time}]' if self.__time_to_move else ''
			return f'Tic Tac Toe² (Ожидается ход от {self.current_player.name})' + time_to_move
		return 'Tic Tac Toe²'