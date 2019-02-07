
# Banjiu 2048

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



### About the game

* a 2048-like tile game, in which you move and combine tiles to bigger ones
* implemented in python, with pygame framework
* usage
```
python ./src/main.py
```

### How to play
* Move blocks with equal values to merge them
* To move the blocks, use these keys: 
  * <kbd>W</kbd> / <kbd>A</kbd> / <kbd>S</kbd> / <kbd>D</kbd>
  * <kbd>H</kbd> / <kbd>J</kbd> / <kbd>K</kbd> / <kbd>L</kbd>
  * <kbd>Up</kbd> / <kbd>Down</kbd> / <kbd>Left</kbd> / <kbd>Right</kbd>
* LEFT board: 
  * has positives (red) and negative (green) tiles
  * red can merge with red tiles; green can merge with greens
  * when a red merges with a green ones, they cancelled out, at the same time, a tile with same face value will spawn in the RIGHT board
* RIGHT board:
  * play just like a normal 2048 game
  * when you get a 2048 in the RIGHT board, you win the game !!!
* Bring up the option (help) menu: <kbd>F1</kbd> or <kbd>Esc</kbd>

### Changelog
* alpha 0.2: 2019-02-06: initial release.

### Todo list
* trophy and achievement system
* effects when a tile spawns
* fix the bug where tiles on LEFT board drop too fast

### Contact
whoji (whoji@null.net)

### Screenshots

Main menu: 
![xxx](./asset/screenshot/screenshot_0.png "main menu" =350x100)

Game view: 
![xxx](./asset/screenshot/screenshot_1.png | width=350)
