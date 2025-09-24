# Project description
This project was created as an assignment for the 2nd week of the Coding Bootcamp for Cybersecurity Professionals.</br>

The goal is to design an API storage system that allows to store and retrieve API keys securely.

# Features 

- Options: save new enrties (service and corresponding API_key) to a data table or look for the API_key of a service in the data table.
- The data table stored in a JSON file and API key are saved in encrypted format. 
...

# Set up the virtual environment

## Mac0S
```
pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

## WindowsOS git-bash CLI

```
pyenv local 3.11.3
python -m venv .venv
source .venv/Scripts/activate
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

* Hint: use `--upgrade` to install packages listed in requirements.txt or update existing to pinned versions
* Add the filekey.key to the .env file
* Add the .env file to the .gitignore file

# How to run the program

Run the program with `python secrets_manager.py` from the command line, an interactive prompt mode allows the following actions until you exit the program.
    1. Save a new entry - 's'
    2. Look for an entry  - 'l'
    3. Exit the program - 'q'


# Disclaimer
This is a WIP, I am still learning (September 2025)
