# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets


class UiMainWindow(object):
    def setupUi(self, MainWindow: QtWidgets.QMainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.setMinimumSize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')

        self.game_label = QtWidgets.QLabel(self.centralwidget)
        self.game_label.setGeometry(QtCore.QRect(250, 100, 340, 80))
        self.game_label.setObjectName('game_label')

        self.play_with_bot_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_with_bot_button.setGeometry(QtCore.QRect(250, 200, 315, 40))
        self.play_with_bot_button.setObjectName('play_with_bot_button')

        self.play_with_player_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_with_player_button.setGeometry(QtCore.QRect(250, 250, 315, 40))
        self.play_with_player_button.setObjectName('play_with_player_button')

        self.play_online_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_online_button.setGeometry(QtCore.QRect(250, 300, 315, 40))
        self.play_online_button.setObjectName('play_online_button')
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'Tic Tac Toe²'))
        self.game_label.setText(_translate('MainWindow', '<html><head/><body><p align=\'center\'><span style=\' font-size:36pt;\'>Tic Tac Toe²</span></p></body></html>'))
        self.play_with_bot_button.setText(_translate('MainWindow', 'Play with bot'))
        self.play_with_player_button.setText(_translate('MainWindow', 'Play with player'))
        self.play_online_button.setText(_translate('MainWindow', 'Play online'))
