# sfia_generator

**To run locally:**

First, clone the project onto your computer with:
`git clone https://gitlab.cs.cf.ac.uk/c1744034/sfia-generator.git`

Install pipenv:
1. Install the pip installer
2. From a command line interface, run `pip install pipenv`

Creating virtual environment:
1.  Navigate to the project folder with your command line interface
2.  Create the virtual environment with `pipenv shell`

When doing any of the following commads below, ensure you're in the virtual environment's shell and in the project's root folder
If not in the shell, navigate to the root folder and run `pipenv shell` from your command line

Setting up libraries
*  While in the shell of the virtual environment, run `pip install -r requirements.txt`

Setting up local SQLite database:
The included settings file (settings.py) is configured to use a local SQLite file as the database by default
*  Run migrations with `python manage.py migrate`

Running the server
*  To run the server locally, while in the virtual environment shell, run the server with `python manage.py runserver`

Creating superuser
*  Create a superuser with `python manage.py createsuperuser` and enter details when prompted

Your server is now set up and you can access it by going to http://localhost:8000 or http://127.0.0.1:8000