# PocketTrainer
The app that lets you build, find, and share workouts

## Install
Ensure you have python3 installed.

Insall Qt5 as follows:
```
sudo apt-get install python3-pyqt5  
sudo apt-get install python3-pyqt5.qtsvg
```

for developing, install a few extra tools:
```
pip3 install --user pyqt5  
sudo apt-get install pyqt5-dev-tools
sudo apt-get install qttools5-dev-tools
```

## Usage
Launch the app by executing
```
./pocket_trainer.py
```

## File system
All of the sub-window widgets are stored in `lib`

The controller class that manages which windows are displayed exists in the main file `pocket_trainer.py'

All images for window icons as well as the workouts are stored in `Images`

