## Simple Mood & Sleep tracker app

Simple mood and sleep tracker app which can be used to track your morning sleep and mood. 

GUI library: Tkinter
Database: SQLite

## Install

To execute install Python

`pip install requirements.txt`

## How to run 

To run application 

`python app.py`

## How to run tests

To run pytest tests

`pytest -v`


## Windows executable

To create Windows executable use pyinstaller

`pip install pyinstaller`

`pyinstaller --paths=venv\Lib\site-packages --onefile --noconsole --windowed --name=MoodTrackerv1 app.py`

EXE file will be created inside dist folder. 

## Mood and Sleep scores

### Mood Score (MS) – From 1 to 10

A scale from 1 (extremely bad mood) to 10 (extremely happy and content.

![image](https://github.com/user-attachments/assets/3b758fe0-7d25-4f52-8b87-96757544948f)

### Sleep Quality Score (SQS)

A Sleep Quality Score (SQS) from 1 to 10, where 1 is severe insomnia and 10 is perfect.

![image](https://github.com/user-attachments/assets/56e7d9cd-e617-4279-91a2-2dfd1be6bb6f)

