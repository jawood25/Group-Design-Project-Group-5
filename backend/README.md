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
