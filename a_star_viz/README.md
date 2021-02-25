# PyGame A* game GUI
This repository contains the implementation on the form of a game with GUI of the A* search algorithm.
> NOTE: Pygame supports `Python version 3.5`. Keep this in mind when creating your virtual environment.

![image](https://github.com/laisbsc/a_star/blob/master/a_star_gui/pygame_astar.gif)

## Install 
To run this repository, please create a virtual environment, activate it, and install the dependencies on `requirements.txt` beforehand.

To install the dependencies:
* Using `pip`:

Run from the root folder on the terminal
```shell
pip install -r requirements.txt`
```
* Using `conda`:
```shell
conda create --name <env_name> --file requirements.txt`
```
> The conda command above creates a virtual environment named <env_name> with the dependencies on the `requirements.txt` file.

## Run
To run the programme and play the game simply run the `a_star.py` file on your favourite IDE or from the terminal use:
```python
python a_star_gui/a_star.py
```
## Play
- The first click to the canvas sets the `start node`, orange coloured square;
- The second click sets the `end node`, cyan coloured square;
- To draw the wall, clock and grag the cursor where you'd like the black dots to appear.
- You can remove a node from the canvas by right clicking on it.
- When finished, set the search function to start by pressing the `space bar`.

Have fun!
