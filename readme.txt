Direction on how to set up the project on a system.

After cloning or pulling this project, 

if you dont have python installed into your computer system, do the following.
1,  Visit google and google PYTHON INSTALLATION WINDOWS/LINUX depending on your operating system
2,  Click on the required link and follow the required directions till you install python unto your system.
3,  If you are using windows, open command prompt and type this command => 
            pip install django
            pip install virtualenvwrapper
    the above commands should be typed one after the other. allow one to run before the other.



Now youre ready for the proper setup

1,      Open the project on VS Code
2,      Open the terminal. Then type the following commands
                mkvirtualenv <Name of the virtual environment>  
                PS: it can be any name for example, mkvirtualenv venv
3,       After running that command, type 
                workon <Name of the virtual environment> 
4,      Type the next command
                pip install -r requirements.txt
5,      Type this command
                python manage.py makemigrations
                python manage.py migrate
6,      Create superuser with this command
                python manage.py cretesuperuser

        Type in your username and password
7,      Type in this command
                python manage.py runserver
        The server should start running.



=>      When the server starts running, visit  http://127.0.0.1:8000/admin
=>      login in with your superuser details

1,      create a chat thread 
                PS: to get the secret field, visit http://127.0.0.1:8000/chat/create/key and copy the code and paste into the secret field
2,      create another user

=>      then you can now start working on the chat.

