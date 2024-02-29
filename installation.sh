#!/bin/bash

# check if python is installed
if ! [ -x "$(command -v python)" ]; then
  echo 'Error: python is not installed.' >&2
  exit 1
fi

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
