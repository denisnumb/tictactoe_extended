main_style = '''
QWidget {
	background-color: #3B4252;
	color: #FFFFFF;
	selection-background-color: #8FBCBB;
}

QCheckBox::indicator {
	height: 25px;
    width: 25px;
	border-radius:4px;
	border-style:solid;
	border-width:2px;
	border-color: #8FBCBB;
}

QCheckBox::indicator:disabled {
	border-color: #3B4252;
	background-color: #252933;
}

QCheckBox::indicator:checked {
  	background-color: #8FBCBB;
}

QCheckBox::indicator:unchecked {
  	background-color: #252933;
}

QRadioButton::indicator {
	height: 25px;
    width: 25px;
	border-radius: 14px;
	border-style: solid;
	border-width: 2px;
	border-color: #8FBCBB;
}

QRadioButton::indicator:disabled {
	border-color: #3B4252;
	background-color: #252933;
}

QRadioButton::indicator:checked {
  	background-color: #8FBCBB;
}

QRadioButton::indicator:unchecked {
  	background-color: #252933;
}

QLineEdit {
	border-width: 2px;
	border-style: solid;
	border-radius: 6px;
	border-color: #8FBCBB;
	background-color: #2E3440;
}

QLineEdit:disabled {
	border-color: #3B4252;
	background-color: #252933;
}

QSpinBox {
	border-radius: 4px;
	border-style: solid;
	border-width: 2px;
	border-color: #8FBCBB;
}

QSpinBox:disabled {
	border-color: transparent;
	background-color: #252933;
}

QSpinBox::up-button {
    width: 15px;
    border-top-right-radius: 4px;
    padding: 4px;
}

QSpinBox::down-button {
    width: 15px;
    border-bottom-right-radius: 4px;
    padding: 4px;
}

QSpinBox::up-button:hover {
    color: #FFFFFF;
    background-color: #8FBCBB;
}

QSpinBox::down-button:hover {
    color: #FFFFFF;
    background-color: #8FBCBB;
}

QSpinBox::up-arrow {
    image: url(:spinbox_up.png);
}
QSpinBox::down-arrow {
    image: url(:spinbox_down.png);
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

zero_color = '#557E8C'
cross_color = '#A7594D'

error_button_style = f'''
QPushButton:disabled {{
	border-color: {cross_color};
	background-color: #252933;
}}
'''

zero_hover_button_style = f'''
QPushButton {{
	border-color: {zero_color};
	background-color: #2E3440;
}}

QPushButton:hover {{
	border-color: #7FB3B7;
	background-color: {zero_color};
}}
'''

cross_hover_button_style = f'''
QPushButton {{
	border-color: {cross_color};
	background-color: #2E3440;
}}

QPushButton:hover {{
	border-color: #7D4B4C;
	background-color: {cross_color};
}}
'''

zero_button_style = f'''
QPushButton:disabled {{
	border-color: {zero_color};
	background-color: {zero_color};
}}
'''

cross_button_style = f'''
QPushButton:disabled {{
	border-color: {cross_color};
	background-color: {cross_color};
}}
'''