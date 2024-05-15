# Boids Simulation – Adaptive Flocking Behavior

This project simulates adaptive flocking behavior using the Boids model, inspired by the seminal work of Craig Reynolds. It includes enhancements such as dynamic neighborhood perception, obstacle avoidance, short-range repulsion, and genetic algorithm optimization.

## Features

- 🧠 Adaptive flocking rules: separation, alignment, cohesion
- 🚧 Obstacle avoidance using vector repulsion
- 🔁 Dynamic perception radius based on surroundings
- 🧬 Genetic algorithm (via DEAP) for behavior optimization
- 🎮 Interactive Pygame interface to tweak parameters live

## Getting Started

### Requirements

- Python 3.x
- `pygame`
- `deap` (for genetic algorithm)

### Installation

```bash
pip install pygame deap
```

### Run the Simulation

```bash
python main.py
```

> Make sure you're in the directory with the simulation script.

## Controls

- **Shift + Click & Drag**: Add obstacles
- **UI Toggles**: Enable/disable flocking rules
- **Parameter Controls**: Adjust perception radius, number of boids, etc.

## Project Structure

```
boids_simulation/
├── main.py
├── boid.py
├── tools.py
├── matrix.py
├── assets/
└── README.md
```

## Research Context

This simulation supports research into heterogeneous swarms and adaptive systems. For full details, refer to the report: *Investigating Adaptive Flocking Behavior using the Boids Model*.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
