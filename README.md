### Installing

1. Clone down this repository and cd into it.
>if you are on a Windows machine, you will need to open the files in your command terminal in order to create the virtual environment.
2. Once inside the repository, cd into `jobsauceEnv` and then cd into `Scripts`
3. Create your virtual environment by typing the command `activate.bat` and then cd back to where you were before `jobsauceEnv`
>you should be back inside the main folder with files called "jobsauceapp, jobsauceEnv, and the README" inside of it.
4. Install the app's dependencies:
```
pip install -r requirements.txt
```
5. Run makemigrations
`python manage.py makemigrations jobsauceapp`

6. Run migrate
`python manage.py migrate`
>This will create all the migrations needed for Django Framework to post items to the database based on the models in the Models/ directory

## Run Server
7. Enter this command and you should be able to access this project on the server specified by your terminal:
`python manage.py runserver `
Ctrl+C to quit

## Questions
>please feel free to find me on LinkedIn or email me if you have questions about getting this up and running. I used a SQlite database and there may be a part of this README missing where I should explain how to create a connection to a database on your machine.
>Thank you for checking it out; happy life and happy job searching, tech friends!

### Thanks
>special thanks goes out to Joe Shep and Steve Brownlee at Nashville Software School for teaching me how to build web apps and answering all my questions as I tried to understand it all enough to build on my own. Love you guys.