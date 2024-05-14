# Performance Tracker Backend

Welcome to the Performance Tracker Backend repository! This repository contains the backend codebase for a performance tracking application. Below are the instructions to set up and run the project.

## Installation

1. **Clone the project**: Begin by cloning this repository to your local machine.

2. **Install Required Dependencies**: Navigate to the project directory and install the required Python dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```

3. **Create Local PostgreSQL Database**: Ensure you have PostgreSQL installed on your system. Create a local PostgreSQL database and update the `.env` file with your database credentials and database name. Modify the following variables in the `.env` file:
   ```
   DB_NAME=db_name
   DB_USER=user
   DB_PASSWORD=password
   DB_HOST=host
   DB_PORT=port
   ```

4. **Apply Database Migrations**: Run the following command to apply the necessary database migrations:
   ```
   python manage.py migrate
   ```

5. **Seed Existing Data**: To seed existing data into the database, run the following command:
   ```
   python manage.py seed_data ad/data/data.json
   ```

6. **Run Server**: Start the development server by running the following command:
   ```
   python manage.py runserver
   ```

## Test

- **Run All Test Cases**: Execute all test cases by running the following command:
  ```
  python manage.py test
  ```

- **Run Specific Test File**: If you want to run specific test files, use the following command:
  ```
  python manage.py test filepath
  ```

