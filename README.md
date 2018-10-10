## EECE 583 Project - Mapping, Placing, and Routing of MCNC Benchmark Circuits to Quantum Annealer Architecture

>Su, J., Tu, T., & He, L. (n.d.). A Quantum Annealing Approach for Boolean Satisfiability Problem. https://doi.org/10.1145/2897937.2897973

[Presentation available here](https://docs.google.com/presentation/d/e/2PACX-1vQks8mPTlgY37H0-BSJRrfL-y1BST5HLqknpHrXkGCHNW6K36bij29vFaozquD183lswUvwttl_tRwd/pub?start=false&loop=false&delayms=3000)

This repo includes the source code for a mapping, placing, and routing workflow for MCNC benchmark circuits to the D-Wave Quantum Annealing architecture. 

The hierarchy of this project is as follows:

#### Mapping
contains the flow for mapping the benchmark circuits to a simplified library and logic for generation of placement input files

#### Placing
contains a genetic algorithm for global cell placement and results of a simulated annealer placer https://github.com/kahlanlg/CADplacement, and the genetic algorithm with and without congestion awareness. Also includes logic for generation of detailed placement/routing input files.

#### Routing
contains a Lee-Moore routing algorithm based on a previous implementation https://github.com/kahlanlg/CADrouting. Also contains results from this algorithm and logic for generation of output files for placement image generation.

#### images
contains logic to generate an output image from the routed result, and images of results obtained for this project. 

#### benchmarks
contains the unmapped MCNC benchmark circuits

#### demo
contains a simple circuit example

#### Execution Instructions
1. clone the repo into your local ABC installation
2. Perform automatic mapping, placing, routing, and image generation by executing ```bash run.sh```

_Dependencies/Credit_
1. ABC http://people.eecs.berkeley.edu/~alanmi/abc/
2. MCNC Benchmark Circuits https://people.engr.ncsu.edu/brglez/
3. Python 2.7
