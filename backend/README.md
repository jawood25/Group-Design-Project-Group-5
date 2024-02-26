# Group-Design-Project-Group-5-backend
```
backend/
├── api/                  # Package for the API module
│   ├── __init__.py       # Module initializer, sets up the Flask application and registers blueprints
│   ├── config.py         # Configuration module, holds settings for various environments (development, production)
│   ├── exts.py           # Extensions module, initializes extensions like SQLAlchemy, Marshmallow, etc.
│   ├── models.py         # Data models module, contains ORM models defining the database schema
│   └── routes.py         # Routes module, includes the routes and view functions for the API endpoints
├── tests/                # Contains all test cases for the application
│   ├── integration/      # Integration tests assessing how different parts of the app work together
│   │   └── ...
│   ├── units/            # Unit tests for individual components of the app
│   │   ├── data/         # Directory for test data files, to be used in test cases
│   │   └── ...
│   └── conftest.py       # Test configuration file used by pytest for setting up test environments
├── utils/                # Utility functions and classes for the app's various operations
│   ├── file/             # Sub-package for file manipulation utilities
│   │   └── ...
│   └── log/              # Sub-package dedicated to logging mechanisms 
│       └── ...
├── README.md             # Comprehensive guide on the project's overview, setup, and usage instructions
├── .env                  # File holding key-value pairs for environment variables, not tracked by version control
├── requirements.txt      # List of all the necessary Python packages for the project, used for easy setup
└── run.py                # Main executable script to start the Flask application server
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

