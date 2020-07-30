# sfia_generator
**Important**

If deploying publicly, please make sure to set debug as false and change the secret key found in `SFIAGenerator/settings/base.py`
or if using Docker, you should edit the debug and secret key settings in the docker.env file

**To run without Docker:**

First, clone the project onto your computer with:
`git clone https://gitlab.cs.cf.ac.uk/c1744034/sfia-generator.git` or `git clone https://github.com/SmilingTornado/sfia_generator.git`

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

**Installing Docker on Ubuntu/Debian (Easy Method):**

If you haven't done it already, clone the project onto your computer with:
`git clone https://gitlab.cs.cf.ac.uk/c1744034/sfia-generator.git` or `git clone https://github.com/SmilingTornado/sfia_generator.git`

If not already in the project directory, change your directory to that of the project with:
`cd sfia_generator`

Run the docker install script with:
`sudo bash docker-compose-install.sh`
This will install Docker and Docker Compose

**Installing Docker on MacOS or Windows:**
Please refer to the documentation at https://docs.docker.com/desktop/

**To run with Docker:**

If you haven't done it already, clone the project onto your computer with:
`git clone https://gitlab.cs.cf.ac.uk/c1744034/sfia-generator.git` or `git clone https://github.com/SmilingTornado/sfia_generator.git`

If not already in the project directory, change your directory to that of the project with:
`cd sfia_generator`

Run the project with:
`docker-compose up -d`

The project will now be running on port 80 of your computer meaning you can access it via http://<Your Server IP> or if running on docker locally, you can use http://localhost or http://127.0.0.1

**Creating a superuser**

On a Unix based system, you can use:
`sudo bash createsuperuser.sh`

On a Windows based system, use:
`docker-compose run web python manage.py createsuperuser --settings=SFIAGenerator.settings.docker`

If unable to use the script on a Unix based system, use:
`sudo docker-compose run web python manage.py createsuperuser --settings=SFIAGenerator.settings.docker`

This will execute a script that will then allow you to insert the login credentials you would like to use

**Uploading a JSON to Skills models**

Navigate to the admin panel via <url>/admin
*  Click on 'Skills jsons'
*  Add your JSON file
*  Tick the box next to the JSON file
*  Select the Action 'Upload to Models'
*  Press Go and wait for it to parse into models


