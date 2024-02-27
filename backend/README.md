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
│   ├── __init__.py       # Module initializer, sets up the test suite
│   ├── integration/      # Integration tests assessing how different parts of the app work together
│   │   └── ...
│   ├── units/            # Unit tests for individual components of the app
│   │   ├── data/         # Directory for test data files, to be used in test cases
│   │   └── ...
│   └── conftest.py       # Test configuration file used by pytest for setting up test environments
├── utils/                # Utility functions and classes for the app's various operations
│   ├── __init__.py       # Module initializer, sets up the utility package
│   └── file/             # Sub-package for file manipulation utilities
│       └── ...
├── __init__.py           # Module initializer, sets up the Flask application and registers blueprints
├── README.md             # Comprehensive guide on the project's overview, setup, and usage instructions
├── .env                  # File holding key-value pairs for environment variables, not tracked by version control
├── .coveragerc           # Configuration file for the coverage tool, used to customize the coverage report
├── requirements.txt      # List of all the necessary Python packages for the project, used for easy setup
├── run_pytest.py         # Script to run the pytest test suite and generate a coverage report
└── run.py                # Main executable script to start the Flask application server
```

## Link to DB
Add config in **\_\_init\_\_.py**

Initialize app and get DB object in **exts.py**


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
