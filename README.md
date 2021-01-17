# retrieve_analytics.py

A helper script for getting YouTube analytic reports.

## Setup

In order to run the script, you need to have the following:

- Python >= 3.8.0, < 3.9.0
- A Google Developers project with the YouTube Analytics API enabled

### Creating a virtual environment

It is recommended you create a virtual environment for the project.

On UNIX-based systems:
```sh
python3.8 -m venv .venv
source ./.venv/bin/activate
```
On Windows:
```powershell
py -3.8 -m venv .venv
./.venv/Scripts/activate
```

## Creating a Google Developers project

1. Follow the instructions on the [YouTube Analytics API docs](https://developers.google.com/youtube/reporting/v1/code_samples/python#set-up-authorization-credentials).
2. Download your secrets file to `data/secrets.json`.

## Installing dependencies

You will need to install the script's dependencies before running it.

1. [Install Poetry](https://python-poetry.org/docs/#installation)
2. Run the following command, making sure the virtual environment is activated:
```sh
poetry install --no-dev
```

If you prefer not to use Poetry, you can install using pip instead:
```sh
pip install google google-api-python-client google-auth-oauthlib pandas
```

## Usage

1. Change directory into the `scripts` directory.
2. To see what options you can parse, run:
```sh
python retrieve_analytics.py -h
```
3. Run the script with the desired options.
4. Open the provided link in the browser, and follow the on-screen instructions.
5. Copy the provided code into the terminal, and press ENTER.

## Contributing

In order to contribute to the project, you will need to install the development dependencies.

Using Poetry:
```sh
poetry install
```
Using pip:
```sh
pip install google google-api-python-client google-auth-oauthlib pandas black mypy
```

Before submitting any code, make sure to run the following command in the root directory of the project:
```sh
black . -l119
```
