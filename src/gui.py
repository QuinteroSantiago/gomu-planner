import tkinter as tk
from tkinter import font
from datetime import datetime, date
from .data_management import load_data, save_data
from .schedule import create_schedule
import src.config as config

# Globals
schedule_display = None
root = None

def run_gui():
    global schedule_display
    global root
    # Main window setup
    root = tk.Tk()
    root.title("Gomu Planner")

    # Define font
    text_font = font.Font(family="Courier New", size=16, weight="bold")
    today = date.today().strftime("%A, %B %d, %Y")

    header_label = tk.Label(root, text=f"{today}", font=text_font)
    header_label.pack(side=tk.TOP, fill=tk.X)
    # Schedule display area
    schedule_display = tk.Text(root, height=20, width=50, font=text_font)
    schedule_display.tag_configure('time', justify='center')
    schedule_display.pack()

    # Define text color tags
    schedule_display.tag_config("current", foreground="green")
    schedule_display.tag_config("past", foreground="red")
    schedule_display.tag_config("future", foreground="grey")

    # Button setup
    view_button = tk.Button(root, text="View Today's Plan", command=update_schedule)
    view_button.pack()

    modify_button = tk.Button(root, text="Modify Plan (TODO)", command=modify_preferences_gui)
    modify_button.pack()

    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.pack()

    update_schedule()

    # Start the GUI event loop
    root.mainloop()


def display_schedule_gui(schedule):
    global schedule_display
    schedule_display.delete('1.0', tk.END)
    now = datetime.now()
    current_time = now.strftime("%H:%M") if now.second % 2 == 0 else now.strftime("%H %M")

    schedule_display.insert(tk.END, f"{current_time} \n\n", "time")
    for start_dt, end_dt, task_name in schedule:
        start_time_str = start_dt.strftime('%H:%M')
        display_text = f"{start_time_str} {task_name}\n"
        if start_dt <= now < end_dt:
            tag_name = "current"
        elif end_dt < now:
            tag_name = "past"
        else:
            tag_name = "future"
        schedule_display.insert(tk.END, display_text, tag_name)

    # Refresh every second
    root.after(1000, lambda: update_schedule())  # Assuming update_schedule handles the time checking

def modify_preferences_gui():
    new_window = tk.Toplevel(root)
    new_window.title("Modify Schedule Preferences")

    # Fetch variable tasks names for dropdown
    options = [task[1] for task in config.variable_tasks]  # Assuming this structure for variable_tasks
    variable = tk.StringVar(new_window)
    variable.set(options[0])  # default value

    opt = tk.OptionMenu(new_window, variable, *options)
    opt.pack()

    entry = tk.Entry(new_window)
    entry.pack()

    button = tk.Button(new_window, text="Save", command=lambda: save_new_time(variable.get(), entry.get(), new_window))
    button.pack()

def update_schedule():
    day_of_week = datetime.today().weekday()
    new_schedule = create_schedule(config.daily_tasks, config.variable_tasks, config.conditional_tasks, day_of_week, config.preferences)
    display_schedule_gui(new_schedule)

def save_new_time(task_name, new_time, window):
    if new_time:
        config.preferences[task_name] = new_time
        save_data(config.preferences_file, config.preferences)
        update_schedule()
    window.destroy()
