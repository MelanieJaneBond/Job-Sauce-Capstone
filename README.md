### Installing

Clone down this repository and cd into it.
>if you are on a Windows machine, you will need to open the files in your command terminal - not the same as Git Bash - in order to create the virtual environment.

Once inside the repository, cd into `jobsauceEnv` and then cd into `Scripts`
Create your virtual environment by typing the command:
```
activate.bat
```
then cd back to where you were before; you should be back inside the folder with files called "jobsauceapp, jobsauceEnv, and the README" inside of it.

### Install the app's dependencies:
```
pip install -r requirements.txt
```
Run makemigrations
```
python manage.py makemigrations jobsauceapp
```
Run migrate
```
python manage.py migrate
```
This will create all the migrations needed for Django Framework to post items to the database based on the models in the Models/ directory

## Run Server
Enter this command and you should be able to access this project on the server specified by your terminal:
```
python manage.py runserver
```
Ctrl+C to quit
p.s. my terminal instructs me that the project is at http://127.0.0.1:8000/ but it runs better at http://localhost:8000/ 

## Questions
Please feel free to find me on LinkedIn or email me `miss.bond2@gmail.com` if you have questions about getting this up and running. I used a SQLite database and there may be a part of this README missing where I should explain how to create a connection to a database on your machine.
Thank you for checking it out; happy life and happy job searching, tech friends!

>Special THANKS goes out to Joe Shep and Steve Brownlee at Nashville Software School for teaching me how to build web apps and answering all my questions as I tried to understand it enough to build on my own. Love you guys.