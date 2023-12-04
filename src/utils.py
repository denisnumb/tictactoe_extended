from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from typing import List
from resources import image_data
from model import x, o, ButtonStyleType
from resources.styles import (
    cross_button_style, 
    zero_button_style,
    cross_hover_button_style,
    zero_hover_button_style,
    default_button_style
)


win_button_styles = {
    x: ButtonStyleType.X_WIN,
    o: ButtonStyleType.O_WIN
}

hover_button_styles = {
    x: ButtonStyleType.X_HOVER,
    o: ButtonStyleType.O_HOVER
}

styles_dict = {
    ButtonStyleType.DEFAULT: default_button_style,
    ButtonStyleType.X_WIN: cross_button_style,
    ButtonStyleType.O_WIN: zero_button_style,
    ButtonStyleType.X_HOVER: cross_hover_button_style,
    ButtonStyleType.O_HOVER: zero_hover_button_style,
}

def set_ttt_button_style(ttt_button, *, style: ButtonStyleType=None, hover_style: ButtonStyleType=None) -> None:
    ttt_button.style = style or ttt_button.style
    ttt_button.hover_style = hover_style or ttt_button.hover_style
    set_button_style(ttt_button.button, [ttt_button.style, ttt_button.hover_style])

def set_button_style(button: QPushButton, styles: List[ButtonStyleType]) -> None:
    if styles:
        button.setStyleSheet(''.join(styles_dict[style] for style in styles))

def set_button_icon(button: QPushButton, symbol: str) -> None:
    icon_path = ':cross.png' if symbol == x else ':zero.png'
    icon = QIcon()
    icon.addPixmap(QPixmap(icon_path), QIcon.Normal)
    icon.addPixmap(QPixmap(icon_path), QIcon.Disabled)
    button.setIcon(icon)