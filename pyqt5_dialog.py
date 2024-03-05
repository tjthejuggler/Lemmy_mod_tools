from PyQt5.QtWidgets import QMessageBox, QApplication
import sys
import json
from datetime import datetime
import os
import math
import time
from PyQt5.QtWidgets import QInputDialog, QLineEdit

dir = '/home/lunkwill/Documents/obsidyen/tail'
obsidian_dir = '/home/lunkwill/Documents/obsidyen/'

def notify(message):
    msg = "notify-send ' ' '"+message+"'"
    os.system(msg)

def make_json(directory):
    directory = os.path.expanduser(directory)
    with open(directory, 'r') as f:
        my_json = json.load(f)
    return my_json

# def get_todays_total_time(type):
#     with open(f'{dir}/{type}_times.txt', 'r') as f:
#         data = json.load(f)
#     todays_total_time = 0
#     for key, value in data.items():
#         todays_total_time += value
#     return todays_total_time

def get_todays_total_time(type):
    with open(f'{dir}/{type}_times.txt', 'r') as f:
        data = json.load(f)
    todays_total_minutes = 0
    for key, value in data.items():
        todays_total_minutes += value // 60  # Convert seconds to minutes
    return todays_total_minutes

def get_current_points(type):
    personal_records_dir = obsidian_dir+'habitsdb.txt'
    personal_records = make_json(personal_records_dir)
    print(personal_records[type])
    todays_date = datetime.now().strftime("%Y-%m-%d")
    return personal_records[type][todays_date]



def increment_habit(self, type):
    todays_total_minutes = get_todays_total_time(type)
    habitsdb_to_add_dir = obsidian_dir+'habitsdb_to_add.txt'
    habitsdb_to_add = make_json(habitsdb_to_add_dir)
    if type == "programming":
        deserved_points = max(1,math.floor(todays_total_minutes / 60 + 0.5))
        current_points = get_current_points("Programming sessions")
        if current_points < deserved_points:
            points_to_add = deserved_points - current_points
            habitsdb_to_add["Programming sessions"] = points_to_add
    elif type == "writing":
        deserved_points = max(1,math.floor(todays_total_minutes / 30 + 0.5))
        current_points = get_current_points("Writing sessions")
        if current_points < deserved_points:
            points_to_add = deserved_points - current_points
            habitsdb_to_add["Writing sessions"] = points_to_add
    elif type == "reading":
        deserved_points = max(1,math.floor(todays_total_minutes / 60 + 0.5))
        current_points = get_current_points("Book read")
        if current_points < deserved_points:
            points_to_add = deserved_points - current_points
            habitsdb_to_add["Book read"] = points_to_add
    elif type == "podcast":
        deserved_points = max(1,math.floor(todays_total_minutes / 60 + 0.5))
        current_points = get_current_points("Podcast finished")
        if current_points < deserved_points:
            points_to_add = deserved_points - current_points
            habitsdb_to_add["Podcast finished"] = points_to_add
    elif type == "drawing":
        deserved_points = max(1,math.floor(todays_total_minutes / 40 + 0.5))
        current_points = get_current_points("Drew")
        if current_points < deserved_points:
            points_to_add = deserved_points - current_points
            habitsdb_to_add["Drew"] = points_to_add
    elif type == "freestyle_juggling":
        deserved_points = max(1,math.floor(todays_total_minutes / 20 + 0.5))
        current_points = get_current_points("Fun juggle")
        if current_points < deserved_points:
            points_to_add = deserved_points - current_points
            habitsdb_to_add["Fun juggle"] = points_to_add

    result = "Pending habits\n"
    for key, value in habitsdb_to_add.items():
        if value > 0:
            result += f"{key}: {value}\n"
    notify(result)
    habitsdb_to_add_dir = os.path.expanduser(habitsdb_to_add_dir)
    with open(habitsdb_to_add_dir, 'w') as f:
        json.dump(habitsdb_to_add, f, indent=4, sort_keys=True)
    time.sleep(1)
    update_theme_script = '~/projects/tail/habits_kde_theme.py'
    update_theme_script = os.path.expanduser(update_theme_script)
    os.system('python3 '+update_theme_script)

def create_backup(type):
    with open(f'{dir}/{type}_times.txt', 'r') as f:
        data = json.load(f)
    with open(f'{dir}/backups/{type}_times_backup.txt', 'w') as f:
        json.dump(data, f, indent=4)

def update_db(time, type):    
    #create the json file if it does not exist
    if not os.path.exists(f'{dir}/{type}_times.txt'):
        with open(f'{dir}/{type}_times.txt', 'w') as f:
            json.dump({}, f)
    create_backup(type)
    # Open the JSON file and load the data
    with open(f'{dir}/{type}_times.txt', 'r') as f:
        data = json.load(f)
    # Get the current date and time in the specified format
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Add a new item with the current date and time as the key and the time variable as the value
    data[current_datetime] = time
    # Save the changes to the JSON file
    with open(f'{dir}/{type}_times.txt', 'w') as f:
        json.dump(data, f, indent=4)

    increment_habit(time, type)
    print(f'Time logged: {time} - {type}')


def ask_log_time(elapsed_time, current_timer_type):
    elapsed_time = elapsed_time // 60  # Convert seconds to minutes
    #remove the .0 from this
    elapsed_time = int(elapsed_time)
    msgBox = QMessageBox()
    msgBox.setWindowTitle('Log Time')
    msgBox.setText(f'Should the time be logged?\n{current_timer_type} - {elapsed_time}')
    yesButton = msgBox.addButton('Yes', QMessageBox.YesRole)
    noButton = msgBox.addButton('No', QMessageBox.NoRole)
    editButton = msgBox.addButton('Edit', QMessageBox.ActionRole)
    msgBox.exec()

    if msgBox.clickedButton() == yesButton:
        print("Yes clicked.")
        update_db(elapsed_time, current_timer_type)
    elif msgBox.clickedButton() == editButton:
        print("Edit clicked.")
        new_elapsed_time, okPressed1 = QInputDialog.getText(None, "Edit elapsed time","Elapsed time:", QLineEdit.Normal, str(elapsed_time))
        new_current_timer_type, okPressed2 = QInputDialog.getText(None, "Edit timer type","Timer type:", QLineEdit.Normal, current_timer_type)
        if okPressed1 and new_elapsed_time.strip().isdigit():
            elapsed_time = int(new_elapsed_time)  # convert string to int
        if okPressed2:
            current_timer_type = new_current_timer_type
        update_db(elapsed_time, current_timer_type)
    else:
        print("No clicked.")

def main():    
    app = QApplication(sys.argv)  # Create an application object only once here
    ask_log_time(20, "Example Type")  # Example call, replace with actual arguments
    sys.exit(app.exec_())  # Start the application's event loop here


if __name__ == '__main__':
    main()
