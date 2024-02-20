# Group-Design-Project-Group-5-backend
```
backend/
├── api/                  # Package for the API module
│   ├── __init__.py       # Module initializer, contains creation and configuration of API
│   ├── exts.py           # Extensions module, used to initialize external extensions like database etc.
│   ├── models.py         # Data models module, contains ORM models for the database
│   └── routes.py         # Routes module, defines API endpoints and view functions
├── README.md             # Project's README file, includes project information, setup instructions, and documentation
├── requirements.txt      # Contains a list of project dependencies to be installed using pip
└── run.py                # The entry point to run the Flask application
```

## How to run the app
Split your terminal. One for frontend and another for backend.

In the backend directory, run `pip install -r requirements.txt`. You can use pip install to install packages.

Run `python run.py`. This is a server-side, which is listening at 3001.

## Link to DB
Add config in **\_\_init\_\_.py**

Initialize app and get DB object in **exts.py**

## Test DB
Modify **test.py** to create test

Typing **http://localhost:3001/api/testdb** in browser to test

## available APIs
**/api/login/** :  for user login

**/api/sign-up/** : for user sign up

**/api/check-login-status/** : for checking user's login status

**/api/upload/** : for uploading user's routes

**/api/userroutes/** : for getting user's created routes

