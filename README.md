![Logo](https://github.com/SHildebrandt4472/Password-checker/blob/main/images/readme_logo.png)

# Task Master 

This is a simple todo app that helps you manage your tasks and stay organized. The app allows you to create, edit, and delete tasks, and provides features like due dates, priority levels, and task categories. It was developed by Sam Hildebrandt for the year 12 Software Engineering task 1.

## How to use Task Master

Task Master is a todo app that includes all of the following featurtes to manage all your tasks that need to get done.

1. Create a task: Click on the "New Task" button and enter the task details such as title, description, due date, priority level, and category.

2. Edit a task: Select a task from the task list and click on the "Edit" button. Update the task details as needed.

3. Delete a task: Select a task from the task list and click on the "Delete" button to remove the task from the app.

4. View task details: Click on a task from the task list to view its details, including the title, description, due date, priority level, and category.

5. Filter tasks: Use the filter options to view tasks based on their priority level or category.

6. Mark task as completed: When a task is completed, click on the checkbox next to the task to mark it as done.

7. Sort tasks: Use the sorting options to arrange tasks based on their due date or priority level.

8. Stay organized: The Task Master app helps you stay organized by providing a clear overview of your tasks and allowing you to manage them efficiently.

Feel free to explore the app and make use of its features to effectively manage your tasks and stay productive.

## Installation

1. Clone the git repo to a local directory

2. Change to the project directory

3. Create a virtual environment in the project directory

```bash
   python -m venv venv
```

4. Activate the virtual environment

```bash
   WINDOWS: venv\Scripts\activate
```

5. Install the required packages

```bash
   pip install -r requirements.txt
```

6. Create the database

```bash  
   flask db upgrade
```

7. Initialize the database with some data

```bash
   flask cli init_data
```

8. Start the app

```bash
   flask run
```

9. Open a browser and navigate to http://127.0.0.1:5000

10. Login with the following credentials

    username: demo
    password: demo

11. You can now use the app

12. To stop the app, press Ctrl+C in the terminal

## License

[License](https://github.com/SHildebrandt4472/Task-Master/blob/main/LICENSE)
