# Aegis

> Modular Aerospace Simulation Platform

Aegis is a modular aerospace simulation platform designed to model and prototype autonomous aerospace missions.

The project was developed as a software engineering portfolio project with a strong emphasis on architecture, modularity and clean design rather than graphical realism.

Current Version: **V1**

---

## Overview

Aegis was created to explore how modern aerospace systems can be modelled using object-oriented software engineering principles.

Instead of creating a simulation for a single mission, the objective is to build a reusable platform capable of supporting multiple aerospace scenarios.

The first implemented mission models the detection and confirmation of forest fires using Earth observation satellites.

Future versions will support additional aerospace missions such as:

- Maritime surveillance
- Search and Rescue (SAR)
- Environmental monitoring
- Border surveillance
- Reconnaissance missions
- Multi-agent autonomous systems

---

## Features

Current version includes:

- Modular simulation engine
- Domain-Driven inspired architecture
- Satellite modelling
- Sensor simulation
- Forest fire entities
- Fire detection engine
- Alert generation
- Simulation snapshots
- Desktop GUI built with PySide6

---

## Architecture

```
                +----------------+
                |   Home Window  |
                +-------+--------+
                        |
                        v
                +----------------+
                | Fire Mission   |
                +-------+--------+
                        |
                        v
                +----------------+
                |  Simulation    |
                +-------+--------+
                        |
                +-------+--------+
                |     World      |
                +-------+--------+
                        |
        +---------------+---------------+
        |                               |
        v                               v
  Satellites                      Fire Entities
        |                               |
        +---------------+---------------+
                        |
                        v
                  Sensor Scan
                        |
                        v
                  Observations
                        |
                        v
                 Detection Engine
                        |
                        v
                  Alert Engine
                        |
                        v
                     Alerts
```

---

## Project Structure

```
Aegis/

│
├── src/
│   ├── domain/
│   │
│   ├── gui/
│   │
│   └── main.py
│
├── assets/
│
├── docs/
│
└── README.md
```

---

## Technologies

- Python 3
- PySide6
- Object-Oriented Programming
- Domain-Driven Design principles
- Git
- GitHub

---

## Design Principles

The project was developed following several software engineering principles:

- Separation of Concerns
- Composition over Inheritance
- Single Responsibility Principle
- Event-based communication
- Incremental development
- Modular architecture

---

## Current Mission

### Forest Fire Detection

The current simulation models:

1. Satellite orbit
2. Sensor observations
3. Fire detection
4. Confidence estimation
5. Alert generation

The GUI allows the user to interact with the simulation through a dedicated mission window.

---

## Future Roadmap

### Version 2

Planned improvements include:

- Interactive map
- Entity creation/removal
- Configurable missions
- Mission editor
- Mission persistence
- Multiple satellite support
- Live simulation controls
- Statistics dashboard

---

## Learning Objectives

The project was developed to strengthen knowledge in:

- Software Architecture
- Object-Oriented Design
- GUI development
- Simulation systems
- Aerospace software engineering

---

## Author

Francisco Oliveira

Aerospace Engineering Student

University of Minho

---

## License

This project is intended for educational and portfolio purposes.