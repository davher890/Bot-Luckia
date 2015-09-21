# Bot-Luckia
Python bot to interact with the Luckia Roulette.

Python bot used to interact with the live roulette in https://www.luckia.es/ruleta-en-vivo/
This bot uses C++ libraries to move the mouse the cursor across the screen and to press left and rigt click button.
Furthermore, It uses the image Python library, to get a screenshot and detemrines color of a pixel and the average color pixel of a cell.
Depending of that hte bot detemrines how to interact with the roulette.

The first step is update the coordinates of the border of the screen, setting the values 'pos_x' and 'pos_y' of the left top corner.

Then compile the Python script and run it by calling the 'run' function.
It takes two optional argumens: the available cash to bet and the value of the minimun bet.

The bot executes a variant of the Martingale betting system (https://en.wikipedia.org/wiki/Martingale_%28betting_system%29)
It begin when three of the same color appears, the it bet to the other color.
If wins, start the process again, if not, double your bet.
When a it's possible to reach a minimun cash of 10, the process stops betting and starts again.

The bot has other features you will discover going deep into the python code.

It is not a way to get rich. The bank always win.
PLAY RESPONSIBLE.
