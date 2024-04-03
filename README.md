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
   DB_HOST=cluster0.b6yu9ji.mongodb.net
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

1. **Navigate to the Backend Director and Execute the Tests**
   - Run the following command to execute the tests. This will trigger the backend tests and display a summary in the terminal:
   ```bash
   cd ./backend
   python run_pytest.py
   ```
     
2. **View Test Coverage and Report**
   - Coverage report.
     - Open `./backend/backend_test/coverage/index.html` to view the coverage report.
   - Summary report.
     - Open `./backend/backend_test/report.html` to view the summary report.


#### Running Frontend Tests

1. **Geeting User Routes**
   - The frontend is running on http://localhost:3000.
   - Go to the login page by clicking the login button on the header.
   - Login with the username: test, password: 1234.
   - Go to the My Account page by clicking the my account button on the header.
   - On the My Account Page, it will show a route uploaded by the user.

## Backend

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


