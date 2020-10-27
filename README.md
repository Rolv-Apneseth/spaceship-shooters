# spaceship-shooters

2D game made with pygame, heavily inspired by space invaders.

## What I learned

- Making a game using pygame
- Building a main menu ui
- Importing assets to use for game models and background
- Use of nested while loops
- Use of OOP

## Installation

1. Requires python 3.6+ to run. Python can be installed from [here](https://www.python.org/downloads/)
2. To download, click on 'Code' to the top right, then download as a zip file. You can unzip using your preferred program.
   - You can also clone the repository using: `git clone https://github.com/Rolv-Apneseth/spaceship-shooters.git`
3. Install the requirements for the program.
   - In your terminal, navigate to the cloned directory and run: `python3 -m pip install -r requirements.txt`
4. To run the actual program, navigate further into the spaceship-shooter folder and run: `python3 main.py`

## Usage

1. In the main menu, you select either start game or OP mode. (OP mode is an easy and exagerated game mode where 100s of enemies spawn but you are practically invincible)
2. When in the game, use wasd to move and spacebar to shoot.

Enemy ships will fly from the top of the screen towards you and shoot lasers in your direction. Destroy the enemy ships before they cross the bottom of the screenor you lose a life.

You lose health both when you get shot by an enemy laser and when you collide with an enemy ship.

The game is lost when you lose either all your health or all your lives.
