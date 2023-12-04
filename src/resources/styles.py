main_style = '''
QWidget {
	background-color: #3B4252;
	color: #FFFFFF;
}
'''

default_button_style = '''
QPushButton {
	color: #FFFFFF;
	border-width: 2px;
	border-radius: 6px;
	border-color: #8FBCBB;
	border-style: solid;
	padding: 4px;
	background-color: #2E3440;
}

QPushButton:hover {
	border-color: #7FB3B7;
	background-color: #3B4252;
}

QPushButton:disabled {
	border-color: #3B4252;
	background-color: #252933;
}
'''

zero_hover_button_style = '''
QPushButton {
	border-color: #8FBCBB;
	background-color: #2E3440;
}

QPushButton:hover {
	border-color: #7FB3B7;
	background-color: #8FBCBB;
}
'''

cross_hover_button_style = '''
QPushButton {
	border-color: #704344;
	background-color: #2E3440;
}

QPushButton:hover {
	border-color: #7D4B4C;
	background-color: #704344;
}
'''

zero_button_style = '''
QPushButton:disabled {
	border-color: #3B4252;
	background-color: #8FBCBB;
}
'''

cross_button_style = '''
QPushButton:disabled {
	border-color: #3B4252;
	background-color: #704344;
}
'''