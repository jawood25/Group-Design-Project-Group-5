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

### User Endpoints

#### `/api/sign-up/`
- **Purpose**: Registers new users.
- **Method**: POST
- **Data Model**: `SignUpModel`
- **Description**: This endpoint registers a new user with a unique username and password.

#### `/api/login/`
- **Purpose**: Authenticates users.
- **Method**: POST
- **Data Model**: `LoginModel`
- **Description**: This endpoint authenticates a user by their username and password, allowing them to log in.

#### `/api/addingfriend/`
- **Purpose**: Adds a friend to a user's friend list.
- **Method**: POST
- **Data Model**: `AddingFriendModel`
- **Description**: This endpoint allows a user to add another user as a friend.

#### `/api/usersfriends/`
- **Purpose**: Fetches a user's friends list.
- **Method**: POST
- **Data Model**: `UsersFriendModel`
- **Description**: This endpoint retrieves the friends list of a specific user.

#### `/api/searchuser/`
- **Purpose**: Searches for users.
- **Method**: POST
- **Data Model**: `UserSearchModel`
- **Description**: This endpoint allows users to search for other users based on username or email.


### Route Endpoints

#### `/api/upload/`
- **Purpose**: Uploads a new route.
- **Method**: POST
- **Data Model**: `UploadRouteModel`
- **Description**: This endpoint allows users to upload a new route with details such as coordinates, map center, city, and comments.

#### `/api/editroute/`
- **Purpose**: Edits an existing route.
- **Method**: POST
- **Data Model**: `EditRouteModel`
- **Description**: This endpoint allows users to edit an existing route's details. It supports updating various fields such as coordinates and city.

- **Method**: DELETE
- **Data Model**: `EditRouteModel`
- **Description**: This endpoint allows users to delete an existing route by providing its route ID.

#### `/api/userroutes/`
- **Purpose**: Fetches routes created by a user.
- **Method**: POST
- **Data Model**: `UserRoutesModel`
- **Description**: This endpoint retrieves all routes created by a specific user.

#### `/api/savingroutes/`
- **Purpose**: Saves a route to a user's profile.
- **Method**: POST
- **Data Model**: `SaveRoutesModel`
- **Description**: This endpoint allows users to save a route to their profile for later viewing.

#### `/api/savedroutes/`
- **Purpose**: Fetches routes saved by a user.
- **Method**: POST
- **Data Model**: `SavedRoutesModel`
- **Description**: This endpoint retrieves all routes saved by a specific user.

#### `/api/searchroute/`
- **Purpose**: Searches for routes based on criteria.
- **Method**: POST
- **Data Model**: `SearchModel`
- **Description**: This endpoint allows users to search for routes based on various criteria such as city, location, and difficulty.

### Comment Endpoints

#### `/api/addingcomment/`
- **Purpose**: Adds a comment to a route.
- **Method**: POST
- **Data Model**: `AddingCommentModel`
- **Description**: This endpoint allows users to add a comment to a specific route.

#### `/api/routescomment/`
- **Purpose**: Fetches comments for a route.
- **Method**: POST
- **Data Model**: `RoutesCommentModel`
- **Description**: This endpoint retrieves all comments associated with a specific route.

### Event Endpoints

#### `/api/uploadevent/`
- **Purpose**: Uploads a new event associated with a route.
- **Method**: POST
- **Data Model**: `UploadEventModel`
- **Description**: This endpoint allows users to create a new event linked to a route.

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