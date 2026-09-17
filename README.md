# Animalia

> An interactive AI-powered platform for exploring the animal kingdom, their habitats, physical characteristics, and geographic distribution.

Animalia is a modern full-stack application designed to make animal knowledge more accessible, visual, and intelligent.

The project combines artificial intelligence, geographic visualization, and structured biological data to create an immersive experience for discovering animals from around the world.

---

## Features

- **AI-Powered Animal Information**

  - Generate detailed information about animals using AI agents.
  - Structured animal data including taxonomy, physical characteristics, habitat, diet, behavior, and conservation status.

- **Interactive 3D Globe**

  - Explore the world using an interactive map-based interface.
  - Visualize animal geographic distributions and natural habitats.
  - Satellite-style visualization for an immersive experience.

- **Animal Search**

  - Search for animals by name, species, or category.
  - Retrieve structured and informative animal profiles.

- **Structured Biological Data**

  - Physical characteristics such as weight, height, lifespan, and body measurements.
  - Habitat and geographical distribution.
  - Taxonomic classification.
  - Conservation and ecological information.

- **AI Agent Architecture**

  - Modular AI agents built with LangGraph.
  - Specialized agents for collecting and processing animal information.
  - Extensible architecture for future intelligent features.

- **Modern Full-Stack Architecture**

  - React frontend.
  - FastAPI backend.
  - Python-based AI services.
  - Interactive map visualization powered by MapLibre GL.

---

# Project Architecture

```text
Animalia/
│
├── bin/
│   ├── ai/
|   |   ├── agents/
|   |   |
|   |   └── tools/
|   |
|   |
|   ├── gui/animalia
|   │   ├── src/
|   │   │   ├── components/
|   │   │   ├── pages/
|   │   │   ├── services/
|   │   │   └── assets/
|   │   └── package.json
|   |
│   |
|   └──server/
|
├── requirements.txt
├── package.json
└── README.md
```

> The exact folder structure may evolve as the project grows.

---

# Technology Stack

## Frontend

| Technology              | Purpose                                  |
| ----------------------- | ---------------------------------------- |
| React                   | User interface                           |
| TypeScript / JavaScript | Frontend development                     |
| MapLibre GL             | Interactive maps and globe visualization |
| Vite                    | Frontend build tool                      |
| CSS                     | Styling and responsive design            |

## Backend

| Technology | Purpose                                |
| ---------- | -------------------------------------- |
| Python     | Backend and AI services                |
| FastAPI    | REST API framework                     |
| Pydantic   | Data validation and structured schemas |
| LangGraph  | AI agent workflows                     |
| LangChain  | LLM integrations and orchestration     |

## Data & Visualization

| Technology            | Purpose                             |
| --------------------- | ----------------------------------- |
| GeoJSON               | Geographic animal distribution data |
| JSON                  | Structured animal information       |
| MapLibre GL           | Geographic visualization            |
| Satellite / Map Tiles | Globe and world visualization       |

---

# Installation

## Prerequisites

Make sure you have the following installed:

- Python 3.11+
- Node.js 18+
- npm or pnpm
- Git

---

## Clone the Repository

```bash
git clone https://github.com/your-username/animalia.git
cd animalia
```

---

# Backend Setup

Navigate to the backend directory.

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the backend directory.

Example:

```env
OPENAI_API_KEY=your_api_key_here
```

Additional environment variables can be added as the project evolves.

> Never commit your `.env` file or API keys to version control.

---

## Running the Backend

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

---

# Frontend Setup

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will typically be available at:

```text
http://localhost:5173
```

---

# MapLibre Configuration

Animalia uses MapLibre GL for interactive geographic visualization.

The application supports:

- Interactive world maps.
- Globe projections.
- Satellite-style map rendering.
- Geographic animal distribution visualization.
- Custom map styles.

Example MapLibre import:

```javascript
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
```

Map styles and geographic data can be configured through JSON style files.

---

# Animal Data Model

Animalia uses structured schemas to represent animal information.

A simplified example:

```python
from pydantic import BaseModel


class AnimalPhysical(BaseModel):
    male_weight: float
    female_weight: float
    max_weight: float
    lifespan: float
```

Animal information can be extended with additional categories such as:

```text
Animal
├── Taxonomy
├── Physical Characteristics
├── Habitat
├── Geographic Distribution
├── Diet
├── Behavior
├── Reproduction
├── Conservation
└── Ecological Importance
```

---

# AI Agent System

One of the core components of Animalia is its AI-powered information retrieval and generation system.

The project uses LangGraph and LangChain to create modular workflows for gathering and processing animal information.

Example conceptual workflow:

```text
User Search
    │
    ▼
Animal Information Agent
    │
    ├── Retrieve Animal Data
    ├── Research Sources
    ├── Validate Information
    └── Structure Response
    │
    ▼
Animal JSON Model
    │
    ▼
FastAPI Backend
    │
    ▼
React Frontend
```

This architecture allows additional specialized agents to be added in the future.

---

# Future Features

Animalia is designed to grow into a comprehensive digital ecosystem for animal discovery and education.

**Note:** For more information of versions, and features take a look at the `ROADMAP.md` file.

# Development Philosophy

Animalia follows several important principles:

### Accuracy

Animal information should be based on reliable scientific sources whenever possible.

### Modularity

The system is designed with independent agents, services, and components that can evolve separately.

### Visual Exploration

Complex biological and geographic information should be presented in an intuitive and engaging way.

### Scalability

The architecture should support future expansion into additional animal species, datasets, AI capabilities, and visualization systems.

---

# Contributing

Contributions are welcome.

To contribute:

1. Fork the repository.
2. Create a new branch.

```bash
git checkout -b feature/new-feature
```

3. Make your changes.
4. Commit your changes.

```bash
git commit -m "Add new feature"
```

5. Push your branch.

```bash
git push origin feature/new-feature
```

6. Open a Pull Request.

---

# License

This project is currently under development.

License information will be added as the project matures.

---

# Project Status

🚧 **Animalia is currently in active development.**

The core architecture, AI agents, backend services, and interactive geographic visualization are being actively developed.

---

# Vision

Animalia aims to become more than just an animal encyclopedia.

The long-term vision is to create an intelligent, interactive digital representation of the animal kingdom — where users can explore species, understand ecosystems, visualize habitats, and discover the incredible diversity of life on Earth.

**Explore. Discover. Understand the animal kingdom.**

---

## Author

@ATMCHGIT18
Developed with curiosity and a passion for technology, artificial intelligence, and the natural world.
