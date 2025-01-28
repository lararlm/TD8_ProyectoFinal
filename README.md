# Optimization of Drainage Area: Heuristic Approaches

### Overview

This project tackles the **Optimization of Drainage Area** problem, where the goal is to strategically position oil extraction machines within a defined area to maximize coverage. This work is based on the work of the Dr. Javier Marenco in his paper "Optimizacion del area de drenaje en yacimientos no convencionales por medio de programacion lineal entera".

The map where we need to put the machines will be represented as a polygon and the machines will be represented as rectangles, where the center of the rectangle will be marked. There are some geographic restrictions that are also represented as polygons.

There are various constraints that we have to keep in mind when we position the machines:
1. The rectangles can´t overlap
2. The center of the rectangles can't be inside the restrictions
3. The totality of the rectangle has to be inside the polygon


We implemented three main heuristics to address this problem:
1. **Grid-Based Placement**
2. **Painting Approach**
3. **Genetic Algorithm**

Each heuristic was designed to balance computational efficiency and solution quality, leveraging Python libraries like Shapely and Matplotlib for geometric and graphical computations.

---

### Heuristics Explained

#### 1. **Grid-Based Placement**
- **Concept:** A grid pattern is generated using the largest extractor size. Adjustments are made iteratively to maximize coverage.
- **Process:**
  - Create an initial grid and filter out invalid placements.
  - Optimize the grid by testing shifted and modified patterns.
  - Use local search to refine the solution by removing and repositioning extractors.
- **Strengths:** Handles large, irregular areas effectively and adapts well to restrictions.

#### 2. **Painting Approach**
- **Concept:** Simulates manual filling of the area by placing extractors contiguously, starting from one corner.
- **Process:**
  - Begin at the bottom-left corner and place extractors left-to-right and bottom-to-top.
  - Skip restricted areas and adjust placement dynamically.
- **Strengths:** Intuitive and performs well with rectangular or simple polygons.


#### 3. **Genetic Algorithm**
- **Concept:** Inspired by Darwinian evolution, this algorithm evolves a population of solutions through selection, crossover, and mutation.
- **Process:**
  - Generate a population of random solutions.
  - Select the best candidates based on fitness (coverage and non-overlap).
  - Combine and mutate solutions to create new generations.
- **Limitations:** Computationally intensive with suboptimal results in this context.


### Future Work

- Enhance heuristic refinement using machine learning.
- Improve computational speed by migrating to C++.
- Explore hybrid algorithms combining grid and painting methods.

---
