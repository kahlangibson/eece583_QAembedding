#!/bin/bash
bash ./Mapping/map.sh
echo "Mapping Complete. Performing Placement..."
python ./Placing/Genetic/main.py 
echo "Placement Complete. Performing Routing..."
python ./Routing/main.py 
echo "Routing Complete. Creating images..."
python ./images/draw.py 
echo "Done!"