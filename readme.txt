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
                python manage.py createsuperuser

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


Data constructs for communicating with the websocket.
=> Connect Logged in User to a chat Thread = data = {}
                                             data.username = logged in user's username
                                             data.chat_id = chat thread id

=> User is Typing =     data = {}
                        data.sender = user's username
                        data.function = 'isTyping'
=> User stopped Typing =            data = {}
                                    data.sender = user's username
                                    data.function = 'notTyping'
=> User deletes message for everyone =          data = {}
                                                data.function = 'delete'
                                                data.message_id = chat message id
                                                data.sender = sender's username
=> User delete message for himself only = GET request to /chat/<chat_id>/message/<message_id>/delete/

=>User sends a message =            data = {}
                                    data.function = 'message'
                                    data.message = message text
                                    data.sender = sender's username
                                    data.sender_id = sender's user_id

=> Message Delivered =          data = {}
                                data.function = 'isDelivered'
                                data.message_id = chat message id
User Online or Offline upcoming....
