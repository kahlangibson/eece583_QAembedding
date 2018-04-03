## EECE 583 Project - Mapping, Placing, and Routing of MCNC Benchmark Circuits to Quantum Annealer Architecture

>Su, J., Tu, T., & He, L. (n.d.). A Quantum Annealing Approach for Boolean Satisfiability Problem. https://doi.org/10.1145/2897937.2897973

This repo includes the source code for a mapping, placing, and routing workflow for MCNC benchmark circuits to the D-Wave Quantum Annealing architecture. 

The hierarchy of this project is as follows:

#### benchmarks
contains the unmapped MCNC benchmark circuits

#### Mapping
contains the flow for mapping the benchmark circuits to a simplified library and logic for generation of placement input files

#### Placement
contains the algorithms for global cell placement, including a previous (Simulated Annealing)[https://github.com/kahlanlg/CADplacement] implementation and a genetic algorithm implementation. Also includes logic for generation of detailed placement/routing input files

_Dependencies/Credit_
1. ABC http://people.eecs.berkeley.edu/~alanmi/abc/
2. MCNC Benchmark Circuits https://people.engr.ncsu.edu/brglez/
