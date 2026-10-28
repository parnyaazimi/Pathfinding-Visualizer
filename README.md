# Discrete Mathematics Project

A Python-based pathfinding game developed as a final project for a university **Discrete Mathematics** course.

## 📌 About the Project

This project demonstrates graph traversal and pathfinding algorithms in a grid-based environment. A player and a target are placed on a grid containing randomly generated walls, and the selected algorithm determines how the player moves toward the target.

The project provides a visual way to explore and compare different search strategies.

## 🧠 Algorithms Implemented

- **Depth-First Search (DFS):** Explores one path as deeply as possible before backtracking.
- **Breadth-First Search (BFS):** Explores neighboring cells level by level and finds a shortest path in an unweighted grid.
- **A* Search:** Uses path cost and a heuristic to guide the search toward the target. This implementation uses Manhattan distance as its heuristic.
- **Bidirectional A* Search:** Performs search from both the player and the target to find a meeting point and construct a path.

## ✨ Features

- Grid-based visual environment built with Pygame
- Randomly generated walls, player position, and target position
- Interactive visualization of the selected pathfinding algorithm
- Validation of movement within the grid and around walls
- Detection of whether the target is reachable
- Victory screen when the player reaches the target

## 🛠️ Technologies Used

- **Python**
- **Pygame**
- Python standard libraries, including `heapq`, `collections`, `random`, and `enum`

## 📁 Project Structure

```text
DescreteMathProject/
├── DM_project_4032.py
├── Player.png
├── Target.png
├── Wall.png
├── Victory.png
└── .gitignore
```

## ▶️ Getting Started

### Requirements

- Python 3.10 or later recommended
- Pygame

### Installation

1. Clone the repository:

   ```bash
   git clone YOUR_REPOSITORY_URL
   ```

2. Navigate to the project directory:

   ```bash
   cd DescreteMathProject
   ```

3. Install Pygame:

   ```bash
   python -m pip install pygame
   ```

4. Run the application:

   ```bash
   python DM_project_4032.py
   ```

### How to Play

When the program starts, choose an algorithm by entering its corresponding number in the terminal:

| Number | Algorithm |
|---|---|
| `1` | DFS |
| `2` | BFS |
| `3` | A* |
| `4` | Bidirectional A* |

The game window displays the grid, player, target, and walls. The selected algorithm then attempts to navigate the player toward the target.

Close the game window to exit.

## Academic Purpose

This project was developed as part of a university Discrete Mathematics course to explore graph traversal, search strategies, heuristic-based pathfinding, and their practical applications.

## 🎓 Academic Information

- **Course:** Discrete Mathematics
- **Academic Level:** Bachelor's Degree — Second Semester
- **Project Type:** Course Project
- **Instructor:** Dr. Leila Azadkhah
- **Project Date:** June ‎2025
---

*Created for educational purposes.*
