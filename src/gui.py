import tkinter as tk
from tkinter import font, ttk, messagebox
import os
from datetime import datetime, date
from .schedule import create_schedule
import chime
from PIL import Image, ImageTk

# Globals
schedule_display = None
root = None
chime.theme('pokemon')
log_timer_id = None
current_active_task = None

def run_gui(config):
    global schedule_display
    global root
    # Main window setup
    root = tk.Tk()
    root.title("Gomu Planner")

    # Add app icon
    script_dir = os.path.dirname(os.path.abspath(__file__))
    planner_dir = os.path.dirname(script_dir)
    image_path = os.path.join(planner_dir, 'public', 'bamboo-logo.jpg')
    logo = Image.open(image_path)
    photo = ImageTk.PhotoImage(logo)
    root.wm_iconphoto(True, photo)
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

    adjust_button = tk.Button(root, text="Adjust Task Time", command=lambda: adjust_time_window(config))
    adjust_button.pack()

    log_button = tk.Button(root, text="Log Activity Now", command=logging_window)
    log_button.pack()

    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.pack()

    update_schedule(config)

    # Start logging timer
    start_logging_timer()

    # Start the GUI event loop
    root.mainloop()


def display_schedule_gui(schedule, config):
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
    root.after(1000, lambda: update_schedule(config))

def adjust_time_window(config):
    new_window = tk.Toplevel(root)
    new_window.title("Modify Schedule Preferences")

    # Fetch variable tasks names for dropdown
    options = [task.task_name for task in config.variable_tasks]  # Access task_name attribute
    variable = tk.StringVar(new_window)
    variable.set(options[0])  # default value

    opt = tk.OptionMenu(new_window, variable, *options)
    opt.pack()

    entry_time = tk.Entry(new_window)
    entry_time.pack()
    # entry_time.insert(0, "HHMM")
    placeholder = "HHMM"

    def on_focus_in(event):
        if entry_time.get() == placeholder:
            entry_time.delete(0, tk.END)
            entry_time.config(fg='black')

    def on_focus_out(event):
        if entry_time.get() == '':
            entry_time.insert(0, placeholder)
            entry_time.config(fg='grey')

    entry_time.insert(0, placeholder)
    entry_time.config(fg='grey')
    entry_time.bind("<FocusIn>", on_focus_in)
    entry_time.bind("<FocusOut>", on_focus_out)

    def save_action():
        time_text = entry_time.get()
        if time_text == placeholder or not time_text:
            messagebox.showerror("Invalid Time", "Please enter a time.")
            return

        try:
            # Ensure input is exactly 4 digits and digits only
            if len(time_text) != 4 or not time_text.isdigit():
                raise ValueError("Please enter time in HHMM format, where HH is hour and MM is minute.")

            # Validate and convert time to datetime.time object
            datetime.strptime(time_text, '%H%M')  # This throws ValueError if invalid

            # Proceed with saving or further processing
            save_new_time(variable.get(), time_text, new_window, config)
        except ValueError as e:
            messagebox.showerror("Invalid Time", f"Invalid time format: {str(e)}")
            return

    button = tk.Button(new_window, text="Save", command=save_action)
    button.pack()


def update_schedule(config):
    global current_active_task
    day_of_week = datetime.today().weekday()
    new_schedule = create_schedule(config.daily_tasks, config.variable_tasks, config.conditional_tasks, day_of_week, config.preferences)

    now = datetime.now()
    new_current_task = None
    for start_dt, end_dt, task_name in new_schedule:
        if start_dt <= now < end_dt:
            new_current_task = task_name
            break

    if new_current_task and new_current_task != current_active_task:
        chime.theme('sonic')
        chime.info()
        chime.theme('pokemon')
        current_active_task = new_current_task

    display_schedule_gui(new_schedule, config)

def save_new_time(task_name, new_time, window, config):
    if new_time:
        config.update_preferences(task_name, new_time)
        update_schedule(config)
    window.destroy()

def start_logging_timer():
    global log_timer_id
    if log_timer_id:
        root.after_cancel(log_timer_id)
    log_timer_id = root.after(1800000, start_logging_timer)  # Schedule next trigger
    logging_window()

def reset_logging_timer():
    global log_timer_id
    if log_timer_id:
        root.after_cancel(log_timer_id)
    log_timer_id = root.after(1800000, start_logging_timer)  # Reset the timer to trigger in 30 minutes

def logging_window():
    chime.info()
    log_window = tk.Toplevel(root)
    log_window.title("Activity Logger")

    # Activities Label
    act_label = tk.Label(log_window, text="What did you do since the last time you logged:")
    act_label.pack()

    # Dropdown menu for predefined activities PRCR = Procrastinated, WRKT = Worked out, exercise, CORE= Corellium work
    activities = ['READ', 'WRKT', 'CORE', 'GOMU', 'PRCR', 'MEAL']
    activity_var = tk.StringVar()
    activity_dropdown = ttk.Combobox(log_window, textvariable=activity_var, values=activities)
    activity_dropdown.set('Choose an activity')  # default value
    activity_dropdown.pack()

    # Text entry for description of the activity
    desc_label = tk.Label(log_window, text="Describe what you did:")
    desc_label.pack()
    desc_entry = tk.Entry(log_window, width=50)
    desc_entry.pack()

    # Save button
    save_button = tk.Button(log_window, text="Save", command=lambda: save_log_entry(activity_var.get(), desc_entry.get(), log_window))
    save_button.pack()
    reset_logging_timer()

def save_log_entry(activity, description, window):
    # Format and append the log entry with a timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} {activity.upper()} - {description}\n"
    with open("activity_log.txt", "a") as file:
        file.write(log_message)
    window.destroy()