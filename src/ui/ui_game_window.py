# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
from typing import List


class UiGameWindow:
	def setupUi(self, Window: QtWidgets.QWidget):
		Window.setObjectName('Tic Tac Toe')
		Window.setMinimumSize(800, 600)

		self.mainGridLayout = QtWidgets.QGridLayout(Window)
		self.mainGridLayout.setContentsMargins(0, 0, 0, 0)
		self.mainGridLayout.setObjectName('mainGridLayout')
		self.mainGridLayout.setSpacing(15)
		
		self.buttons: List[List[QtWidgets.QPushButton]] = []
		self.buttons_flat: List[QtWidgets.QPushButton] = []

		positions = [(i, j) for i in range(3) for j in range(3)]

		for grid_index, (grid_row, grid_colum) in enumerate(positions):
			gridLayout = QtWidgets.QGridLayout()
			gridLayout.setObjectName(f'{grid_row}{grid_colum}')
			gridLayout.setSpacing(3)
			self.buttons.append([])

			for row, col in positions:
				button = QtWidgets.QPushButton(Window)
				button.setObjectName(f'{grid_index}{row}{col}')
				sizePolicy = QtWidgets.QSizePolicy(
					QtWidgets.QSizePolicy.Expanding, 
					QtWidgets.QSizePolicy.Expanding
				)
				button.setSizePolicy(sizePolicy)
				button.setIconSize(QtCore.QSize(40, 40))
				gridLayout.addWidget(button, row, col, 1, 1)
				self.buttons[grid_index].append(button)
				self.buttons_flat.append(button)

			self.mainGridLayout.addLayout(gridLayout, grid_row, grid_colum, 1, 1)


		self.retranslateUi(Window)
		QtCore.QMetaObject.connectSlotsByName(Window)

	def retranslateUi(self, Window):
		Window.setWindowTitle('Tic Tac Toe²')
