# Group Design Project - Group 5

Repository for Group 5 in the CSU44098 Group Design Project module.

## Step by Step

### How to run the app

Follow these steps to run the app. You'll need to split your terminal into **two**:

` one for the frontend and another for the backend. `

#### Backend Setup

1. **Navigate to the Backend Directory**
   ```bash
   cd ./backend
   ```
2. Install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```
3. **Create a .env file**
   - Create a file named `.env` in the backend directory.
   - Add the following content to the file:
   ```
   DB_NAME=pathpal
   DB_HOST=mongodb+srv://cluster0.b6yu9ji.mongodb.net
   DB_USERNAME=[YOUR_USERNAME]
   DB_PASSWORD=[YOUR_PASSWORD]
   ```
   - Replace `[YOUR_USERNAME]` and `[YOUR_PASSWORD]` with given an username and a password in **Backends** section.

4. Start the backend server by running:
   ```bash
   python run.py
   ```
   - The server-side is listening at port `3001`.

#### Frontend Setup

1. **Navigate to the Frontend Directory**
   ```bash
   cd frontend
   ```
2. Install the required dependencies using npm:
   ```bash
   npm install
   ```
3. Start the frontend by running:
   ```bash
   npm start
   ```
- If you see the message from Flask on `http://localhost:3000`, it means everything is working correctly!

### How to test the app

#### Backend Testing

#### Running Backend Tests
1. **create .coveragerc file**
   - create a file named `.coveragerc` in the backend directory.
   add the following content to the file:
   ```
   [run]
   omit =
       __init__.py
       test_*.py
       run*.py
       */tests/*
       */utils/*
   ```

2. **Execute the Tests**
   - Run the following command to execute the tests. This will trigger the backend tests and display a summary in the terminal:
   ```bash
    python ./backend/run_pytest.py
   ```
     
3. **View Test Coverage and Report**
   - Coverage report.
     - Open `./backend/coverage/index.html` to view the coverage report.
   - Summary report.
     - Open `./backend/report.html` to view the summary report.
†

#### Running Frontend Tests

## Backends

### Flask
 Running on http://localhost:3001

 More information about API [here](./backend/README.md)

### DataBase
 **MongoDB** is used as the database for this project.
 
information about the database:
 ```
 DB_USERNAME=PathPalAdmin
 DB_PASSWORD=YOAybG23XVTqQnri
 ```


