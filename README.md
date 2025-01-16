# Real-Time Chat Application

This is a real-time chat application built using *Django, **WebSockets* (via Django Channels), and *PostgreSQL*. The app allows users to register, log in, and engage in real-time messaging with other users. The message history is stored in the database, making it available even after a user refreshes the page.

## Features

- *User Authentication*: Users can sign up, log in, and access their individual chat profiles.
- *Real-Time Messaging*: Using WebSockets for real-time communication between users.
- *Chat History*: All chat messages are saved in the database and can be retrieved.
- *User Interface*: A simple, easy-to-use interface with a chat window and message input area.

## How it Works

1. *User Registration*: Users can create an account with a username and password.
2. *Login*: After registration, users can log in to the platform to access the chat functionality.
3. *Selecting a User*: Once logged in, users can select other users from the list of available users.
4. *Real-Time Messaging*: Users can send and receive messages instantly through the WebSocket connection.
5. *Message History*: Previous messages between users are displayed as soon as they initiate a chat session.

## Technologies Used

- *Django*: A high-level Python web framework for rapid development.
- *Django Channels*: Extends Django to handle WebSockets, enabling real-time communication.
- *PostgreSQL*: Relational database to store user data and chat messages.
- *HTML/CSS*: Frontend markup and styling for the user interface.
- *JavaScript*: Client-side logic for handling real-time messaging.

## Setup Instructions (For Developers)

If you want to set up this project on your local machine, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yvr1234/Project.git

2. Navigate to the project directory:

cd chat-application


3. Set up a Python virtual environment:

python -m venv venv


4. Activate the virtual environment:

For Windows:

.\venv\Scripts\activate

For macOS/Linux:

source venv/bin/activate



5. Install the required dependencies:

pip install -r requirements.txt


6. Set up the database and run migrations:

python manage.py migrate


7. Create a superuser to access the Django admin panel:

python manage.py createsuperuser


8. Run the development server:

python manage.py runserver


9. Open your web browser and go to http://127.0.0.1:8000 to access the application.



Usage

Once the app is running:

Open http://127.0.0.1:8000 in your web browser.

Sign up for a new account or log in if you already have one.

After logging in, select a user from the available list and start chatting.
