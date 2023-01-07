# Import libraries needed later on in the code here.
from datetime import date
from datetime import datetime
import math

# === Define all functions ===

# Create and define function 'login'.
def login():
    # Call in the global variables to use in the function.
    global user_name
    global logged_in

    # Open the text file containing user names and passwords.
    # Use for loop to add the data to a file, check against this file to see if username and password match.
    with open("user.txt", "r") as file:
        user_names = []
        user_list = file.readlines()
        for user in user_list:
            user = user.split(", ")
            user_names.append(user[0])
        if user_name in user_names:
            password = input("Please enter your password: ")
            for user in user_list:
                user = user.split(", ")
                user[1] = user[1].strip("\n")
                if user[0] == user_name and user[1] == password:
                    logged_in = True
                    return
            print("Password incorrect.")
            return
        else:
            user_name = input("Incorrect username, please enter your username: ")
            return


# Create a function for registering a new user.
def reg_user():
    while user_name == "admin":
        new_username = input("Please enter a new username: ")
        with open("user.txt", "r") as file:
            new_username = file.readlines()
            print("This username already exists, please try another username.")
            new_username = input("Please enter a different username: ")
        new_passw = input("Please enter a password: ")
        confirm_pw = input("Please confirm the password: ")
        if new_passw != confirm_pw:
            confirm_pw = input("The password didn't match the first one, please confirm your password again: ")
        elif new_passw == confirm_pw:
            user_new = f"\n{new_username}, {new_passw}"
            with open("user.txt", "a") as user:
                user.write(user_new)
                print("User has now been added to the database.")
                break
    if user_name != "admin":
        print("You are not allowed to register new users.")
        return

# Create a function for user to add a task to the text file tasks.txt.
def add_task():
    new_task = input('''Please enter the username of the person the task is assigned to,
    title of the task, description of the task,
    please separate each part with a comma followed by space:\n ''').lower()
    new_task_due = input("When is this task due, please write in format '15 Dec 2022': ")
    with open("tasks.txt", "a") as task:
        today = date.today()
        current_date = date.today()
        today = today.strftime("%d %b %Y")
        task.write(f"\n{new_task}, {today}, {new_task_due}, No")
        return


# Create a function to view all tasks in the tasks file.
def view_all():
    with open("tasks.txt", "r") as tasks:
        for line in tasks:
            all_tasks = line.split(", ")
            name = all_tasks[0]
            task = all_tasks[1]
            description = all_tasks[2]
            start_date = all_tasks[3]
            due_date = all_tasks[4]
            complete = all_tasks[5]
            print(f"""
    Task:           {task}
    Assigned to:    {name}
    Date assigned:  {start_date}
    Due date:       {due_date}
    Task complete?  {complete}
    Task description:\n{description}
    """)
    print("===================================================================")
    return


# Create a function to view the current user's tasks in the tasks file.
def view_mine():
    with open("tasks.txt", "r") as tasks:
       for i, line in enumerate(tasks, start = 1):
           all_tasks = line.split(", ")
           name = all_tasks[0]
           task = all_tasks[1]
           description = all_tasks[2]
           start_date = all_tasks[3]
           due_date = all_tasks[4]
           complete = all_tasks[5]
           if user_name == name:
               print(f"""{i}:
Task:           {task}
Assigned to:    {name}
Date assigned:  {start_date}
Due date:       {due_date}
Task complete?  {complete}
Task description:\n{description}
""")

    print("=========================================================================")
    return

# Create a function to mark a task as complete.
def task_complete(task_num):
    # Cast the input variable to int, and then declare other variables needed.
    task_num = int(task_num)
    task_counter = 1
    output_data = ''

    # Open the tasks file using with-as.
    with open('tasks.txt', 'r') as task_file:

        # Everytime the loop runs, it checks if the task belongs to the user logged in
        # If the task is assigned to the user logged in, the complete is marked as 'Yes'.
        for line in task_file:
            task_contents = line.replace('\n', '').split(', ')
            if task_contents[0] == user_name:
                if task_num != task_counter:
                    output_data += line

                else:
                    for item in range(0, 5):
                        output_data += task_contents[item] + ', '

                    output_data += 'Yes\n'

                # Only increment this counter if the task belongs to the current user.
                task_counter += 1

            else:
                output_data += line

    # Open the tasks file and write over it with the updated data.
    with open('tasks.txt', 'w') as task_file:
        task_file.write(output_data)

    # Inform the user that the task has been marked as completed.
    print("Task #{} has been marked as completed.".format(task_num))


# Create a function to allow user to edit a task.
def edit_task(task_num):
    # Cast input variable to integer, declare other variables.
    task_num = int(task_num)
    task_counter = 1
    output_data = ''

    # Open file as read only.
    with open('tasks.txt', 'r') as task_file:

        # Loop through the file and split line contents into a list.
        for line in task_file:
            task_contents = line.replace('\n', '').split(', ')

            # Check if the task is assigned to the current user, otherwise add the line to the output.
            if task_contents[0] == user_name:

                # Make sure the task is the selected one and one that hasn't been marked as complete already.
                if task_num != task_counter:
                    output_data += line

                elif task_num == task_counter and task_contents[5] == 'Yes':

                    print("You cannot edit a task that has already been completed.")
                    output_data += line

                else:
                    # If the task can be edited, ask for the appropriate task as well as the new data entry.
                    user_choice = input("Would you like to edit the Assigned user (A) or the Due date (D)? ")

                    # Append the output with the appropriate data, depending on user's choice.
                    if user_choice.lower() == 'a':

                        new_entry = input("Please enter the new user to assign to this task: ")
                        output_data += new_entry + ', '

                        for item in range(1, 5):
                            output_data += task_contents[item] + ', '

                        output_data += task_contents[5] + '\n'
                        print("Task successfully edited.")

                    elif user_choice.lower() == 'd':

                        new_entry = input("Please enter the new due date for this task: ")

                        for item in range(0, 4):
                            output_data += task_contents[item] + ', '

                        output_data += new_entry + ', No\n'
                        print("Task successfully edited.")

                    # If incorrect choice is made, no change is made and print appropriate statement.
                    else:
                        print("Invalid selection. Please try again.")
                        output_data += line

                # Only increment this counter if the task belongs to the current user.
                task_counter += 1

            else:
                output_data += line

        # Now write the output to the file.
        with open('tasks.txt', 'w') as tasks_file:
            tasks_file.write(output_data)

# Create a function to generate reports out of the data stored in the text files, store these in new text files.
def generate_reports():

    # Declare variables for the function.
    total_tasks = 0
    completed_tasks = 0
    incomplete_tasks = 0
    overdue_tasks = 0
    user_list = []
    user_output = ''

    # Populate the user list with a loop and a with/as block.
    with open('user.txt', 'r') as user_file:

        for line in user_file:
            line_contents = line.split(', ')
            user_list.append(line_contents[0])

    # Open tasks file for reading only.
    with open('tasks.txt', 'r') as task_file:

        for line in task_file:

            # Newline characters are stripped and items are placed in a list.
            task_contents = line.replace('\n', '').split(', ')

            # Items in the lists are stored in appropriately named variable.
            user_assigned = task_contents[0]
            task_due_date = datetime.strptime(task_contents[4], "%d %b %Y")
            completion_status = task_contents[5]

            # Check if task is complete or overdue.
            if completion_status == 'Yes':

                total_tasks += 1
                completed_tasks += 1

            else:

                if datetime.now() > task_due_date:

                    total_tasks += 1
                    incomplete_tasks += 1
                    overdue_tasks += 1

                else:

                    total_tasks += 1
                    incomplete_tasks += 1

    # Calculate percentages.
    incomplete_percentage = round((incomplete_tasks / total_tasks) * 100)
    overdue_percentage = round((overdue_tasks / total_tasks) * 100)

    # Create/write to the appropriate file.
    with open('task_overview.txt', 'w+') as task_overview_file:
        task_overview_file.write('''Total number of tracked tasks: {}
Total number of completed tasks: {}\nTotal number of incomplete tasks: {}
Total number of overdue tasks: {}\nPercentage of tasks that are incomplete: {}%
Percentage of tasks that are overdue: {}%'''.
                                 format(total_tasks, completed_tasks, incomplete_tasks,
                                        overdue_tasks, incomplete_percentage,
                                        overdue_percentage))

    # Begin forming the contents of the user overview file.
    user_output = '''Total number of registered users: {}
Total number of tracked tasks: {}\n'''.format(len(user_list), total_tasks)

    # Loop through all users.
    for user in user_list:

        # Declare variables.
        user_tasks_total = 0
        user_tasks_completed = 0
        user_tasks_incomplete = 0
        user_tasks_overdue = 0

        # Loop through the file for every user. Every iteration stores data that is needed for the overview file.
        with open('tasks.txt', 'r') as task_file:

            for line in task_file:

                # Split the contents of the line and remove newlines.
                task_contents = line.replace('\n', '').split(', ')

                # Items in the lists are stored in appropriately named variable.
                user_assigned = task_contents[0]
                task_due_date = datetime.strptime(task_contents[4], "%d %b %Y")
                completion_status = task_contents[5]

                # Depending on the completion status, or if the task is overdue, different values will be altered.
                if user_assigned == user:
                    user_tasks_total += 1
                    if completion_status == 'No' and datetime.now() > task_due_date:
                        user_tasks_incomplete += 1
                        user_tasks_overdue += 1
                    elif completion_status == 'No' and datetime.now() < task_due_date:
                        user_tasks_incomplete += 1
                    else:
                        user_tasks_completed += 1

        # Calculate percentages for users with at least 1 task, or if no tasks assigned for the user, all equals 0.
        if user_tasks_total > 0:
            task_assigned_percentage = round((user_tasks_total / total_tasks) * 100)
            completed_assigned_percentage = round((user_tasks_completed / user_tasks_total) * 100)
            incomplete_assigned_percentage = round((user_tasks_incomplete / user_tasks_total) * 100)
            overdue_assigned_percentage = round((user_tasks_overdue / user_tasks_total) * 100)
        else:
            task_assigned_percentage = 0
            completed_assigned_percentage = 0
            incomplete_assigned_percentage = 0
            overdue_assigned_percentage = 0

        # Finalise the data of this user into the output string.
        user_output += '''User: {}
            \tTotal assigned tasks: {}
            \tPercentage of total tasks assigned to {}: {}%
            \tPercentage of assigned tasks completed: {}%
            \tPercentage of assigned tasks incomplete: {}%
            \tPercentage of assigned tasks overdue: {}%\n'''.format(user, user_tasks_total,
                                                                    user, task_assigned_percentage,
                                                                    completed_assigned_percentage,
                                                                    incomplete_assigned_percentage,
                                                                    overdue_assigned_percentage)

    # Create/overwrite the user overview file using the final output.
    with open('user_overview.txt', 'w+') as user_overview_file:
        user_overview_file.write(user_output)

    # Indicate to the user that the process is complete.
    print("Reports have been generated.")

# ===== LOGIN =====
# Ask the user to enter their username to log in.
user_name = input("Please enter your username: ")

# Set logged in as False by default, unless the following steps are met and then it becomes True and lets the user in.
logged_in = False

# If the user is unable to provide correct username and password, call function 'login' again.
while not logged_in:
    login()

# ===== MAIN MENU =====
# Once user is logged in, present the menu to the user, make sure input is converted to lower case.
while True:
    print("=============================================================")
    if user_name == "admin":
        menu = input('''\nSelect one of the following options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Statistics
e - Exit
: ''').lower()

    elif user_name != "admin":
        menu = input('''\nSelect one of the following options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
e - Exit
: ''').lower()

    # If the user chooses 'r', call out the function for 'reg_user'.
    if menu == "r":
        reg_user()


    # If the user chooses 'a', call out the function for 'add_task'.
    elif menu == "a":
        add_task()


    # If the user chooses 'va', open and read all the tasks from the task text file, print these.
    elif menu == "va":
        view_all()


    # If the user chooses 'vm', open the task text file and print the task information assigned to the user.
    elif menu == 'vm':
        user_choice = ''
        while user_choice != '-1':
            view_mine()
            user_choice = input("Which task would you like to select? Type '-1' to return. ")
            if user_choice != '-1':
                user_action = input("Would you like to edit Task #{} (E) or mark it as complete (M)? ".
                                    format(user_choice))
                if user_action.lower() == 'e':
                    edit_task(user_choice)
                elif user_action.lower() == 'm':
                    task_complete(user_choice)
                else:
                    print("Invalid selection. Please try again.")


    # If the user admin chooses 'ds', display all statistics.
    elif menu == 'ds':

        # Check if current user is an admin, and if he is, the program will proceed.
        if user_name == 'admin':

            # Call the generate reports function.
            generate_reports()

            # Print the contents of both the task overview and user overview files.
            print("=================\nTask Overview:\n=================")

            with open('task_overview.txt', 'r') as task_overview_file:

                for line in task_overview_file:
                    print(line.replace('\n', ''))

            print("=================\nUser Overview:\n=================")

            with open('user_overview.txt', 'r') as user_overview_file:

                for line in user_overview_file:
                    print(line.replace('\n', ''))

        else:
            print("You have made a wrong choice, please try again.")


    # Generating reports:
    elif menu == 'gr':

        # Check if current user is an admin, and if he is, the program will proceed.
        if user_name == 'admin':
            generate_reports()

        else:
            print("You have made a wrong choice, please try again.")


    # If the user chooses 'e', exit the program.
    elif menu == "e":
        print('Goodbye!!!')
        exit()

    # If the user had entered an invalid option, ask them to try again.
    else:
        print("You have made a wrong choice, please try again.")
