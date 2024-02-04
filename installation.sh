#!/bin/bash

# Liste der Module
MODULES=(
 "numpy==1.26.3"
 "opencv-contrib-python==4.9.0.80"
 "opencv-python==4.9.0.80"
 "pillow==10.2.0"
)

# Installieren oder Aktualisieren der Module
for MODULE in "${MODULES[@]}"
do
 echo "Installiere oder aktualisiere $MODULE..."
 pip install --upgrade "$MODULE"
done
