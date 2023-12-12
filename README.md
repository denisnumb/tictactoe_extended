# Tic Tac Toe²

# Правила игры в Tic Tac Toe².
---
Игра ведется на сетке состоящей из 9 полей, 3 на 3 клетки:

![image](https://github.com/denisnumb/tictactoe_extended/assets/108686703/4ea964c0-47c1-4a32-91db-3e5ba66b3d7d)

Каждое поле является отдельным полем игры в "крестики-нолики", обособленным по отношению к другим.

Игра ведётся игроками по очереди, 1-ый игрок выбирает 1 из 9 полей с которого начнётся игра.

Выбранная каждым игроком клетка в поле, отсылает следующего игрока на соответствующую позицию поля в сетке:

![image](https://github.com/denisnumb/tictactoe_extended/assets/108686703/686407dd-87e0-4462-a931-f406a3318ee3)

При заполнении поля, оно блокируется и принимает значение одного из игроков или ничьей.

При переходе хода на заблокированное поле, ход переходит на ближайшее свободное поле:

*Пример 1*
![image](https://github.com/denisnumb/tictactoe_extended/assets/108686703/33304e86-4acc-4492-aaec-496c1f56d9e4). *Пример 3*
