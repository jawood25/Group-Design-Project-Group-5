# Group-Design-Project-Group-5-backend
```
backend/
├── api/                  # Package for the API module
│   ├── __init__.py       # Module initializer, sets up the Flask application and its configuration
│   ├── config.py         # Configuration module, contains the configuration settings for the app
│   ├── exts.py           # Extensions module, initializes and configures the app's extensions
│   ├── models.py         # Data models module, contains ORM models defining the database schema
│   └── routes.py         # Routes module, includes the routes and view functions for the API endpoints
├── tests/                # Contains all test cases for the application
│   ├── integration/      # Integration tests for the app's various features
│   │   └── ...
│   └── unittest/         # Unit tests for individual components of the app
│       ├── test_models/  # Test cases for the data models and their methods
│       │   ├── data/     # Test data used by the test cases
│       │   └── ...
│       ├── test_routes/  # Test cases for the API routes and their view functions
│       │   ├── data/     # Test data used by the test cases
│       │   └── ...
│       └── conftest.py   # Test configuration file used by pytest for setting up test environments
├── utils/                # Utility functions and classes for the app's various operations
│   └── file/             # Sub-package for file manipulation utilities
│       └── ...
├── README.md             # Guide on the backend's overview and usage instructions
├── .env                  # File holding key-value pairs for environment variables
├── .coveragerc           # Configuration file for the coverage tool, used to customize the coverage report
├── requirements.txt      # List of all the necessary Python packages for the project, used for easy setup
├── run_pytest.py         # Script to run the pytest test suite and generate a coverage report
└── run.py                # Main executable script to start the Flask application server
```

## API Endpoints

### `/api/sign-up/`
- **Purpose**: User registration
- **Method**: POST
- **Data Model**: `SignUpModel`
- **Description**: Registers new users with a unique username and password.

### `/api/login/`
- **Purpose**: User login
- **Method**: POST
- **Data Model**: `LoginModel`
- **Description**: Authenticates users by username and password.

### `/api/upload/`
- **Purpose**: Route upload
- **Method**: POST
- **Data Model**: `UploadModel`
- **Description**: Allows users to upload new routes with detailed information.

### `/api/userroutes/`
- **Purpose**: Fetch user-created routes
- **Method**: POST
- **Data Model**: `UserRoutesModel`
- **Description**: Retrieves routes created by a specified user.

## Setting Up the Database
1. Create an account on MongoDB Atlas.
2. Create a free shared cluster with default settings.
3. Create a new project if one hasn't already been created.
4. Click the Database tab on the left and select the free database.
5. You will be prompted to create an admin user, save the password somewhere for later.
6. Add the IP address "0.0.0.0" so that anyone can connect to the database or a specific one from a specific machine and continue.
5. Once the database has been created, go to the Overview tab and click on the connect button.
7. Connect to the application via Drivers and select the Python driver. Choose the most stable version and copy the connection string.
8. Replace "\<password>" in the connection string with the previously saved admin password
9. Create a .env file in the backend directory with the following format:
```
DB_NAME=pathpal
DB_HOST=host
DB_USERNAME=user
DB_PASSWORD=password
```
10. Take the admin name from the connection string and replace user in the .env file with it. Delete the colon after it.
11. Take the password from the connection string and replace password in the .env file with it. Delete the "@" after it.
12. Delete everything after "mongodb.net/" in the connection string and use what is left to replace host in the .env file. Append "palpath" after it so a collection named "palpath" is created when any data is stored.