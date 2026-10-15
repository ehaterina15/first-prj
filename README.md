# Snake

**The classic Snake game written in Python with Pygame, built around a small object-oriented design.**

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.6-green)
![Code style](https://img.shields.io/badge/code_style-PEP8%20%2F%20flake8-brightgreen)

## Gameplay

- Steer the snake with the **arrow keys**
- Eat the red apple to grow by one segment
- The field wraps around: leaving one edge brings you back on the opposite side
- Running into your own body resets the game
- The apple never spawns on top of the snake

## Design

The game uses a small class hierarchy:

```
GameObject            # base class: position, colour, draw()
├── Apple             # random placement on the grid
└── Snake             # segments, direction, move(), growth, self-collision, reset()
```

The main loop handles input, updates the snake, checks for collisions with the apple, and redraws the 640×480 grid at a fixed tick rate.

## Run it

```bash
git clone https://github.com/ehaterina15/first-prj.git
cd first-prj
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python snake.py
```

## Context

My first Python project, from the [Yandex Practicum](https://practicum.yandex.com/) Python course. It covers OOP basics (inheritance, encapsulation), working with a game loop and keeping the code PEP 8 / flake8 clean.

## Author

**Ekaterina Mashentseva** · [GitHub](https://github.com/ehaterina15)
