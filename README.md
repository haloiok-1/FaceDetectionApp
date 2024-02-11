# Project Title: Person Detection and Recognition

## Overview
This project is aimed at developing a system for detecting and recognizing 
persons using computer vision techniques.
The system includes functionalities such as capturing photos,
training the model for face recognition,
and detecting faces in real-time video streams. 
It also allows users to set profile pictures for identified persons.


## Technologies Used
- Python
- OpenCV
- Tkinter
- PIL (Python Imaging Library)
- NumPy

## Project Structure
The project consists of several Python scripts organized as follows:

### 1. Main Application (App.py)
- Manages the GUI and orchestrates the functionalities of the system.
- Provides interfaces for user input and interaction.
- Coordinates photo capturing, face training, and face detection.

### 2. Face Detector (FaceDetector.py)
- Detects faces in real-time video streams using OpenCV's Haar Cascade classifier.
- Utilizes a pre-trained LBPH (Local Binary Patterns Histograms) face recognizer for face recognition.
- Displays the camera feed with detected faces and recognized persons.

### 3. Photo Taker (Phototaker.py)
- Controls the capturing of photos using the system's camera.
- Allows users to take photos, set profile pictures, and save captured images.
- Manages the directory structure for storing photos of different persons.

### 4. Trainer (Trainer.py)
- Trains the face recognition model using captured photos.
- Utilizes LBPH face recognition algorithm for training.
- Saves the trained model and associated labels for future recognition tasks.

### 5. Person Class (Person.py)
- Represents a person with attributes such as name, age, gender, and photo directory.
- Encapsulates methods for setting profile pictures and managing photo folders.

### 6. Additional Dependencies (requirements.sh)
- Specifies the required Python modules and their versions for the project.
- Facilitates installation or upgrade of dependencies using pip.

## Usage
To run the project:
1. Ensure Python and required dependencies are installed.
2. Execute the main application script `App.py`.
3. Interact with the GUI to perform various tasks such as capturing photos, training the model, and detecting faces.

## Future Enhancements
- Implement more robust face detection and recognition algorithms.
- Enhance the user interface for better user experience.
- Integrate additional features such as age and gender estimation.
- Optimize performance for real-time processing on resource-constrained devices.

## Contributors
- Czylonio

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
