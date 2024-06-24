from datetime import datetime, timedelta, date

def create_schedule(daily_tasks, variable_tasks, conditional_tasks, day_of_week, preferences):
    today_date = date.today()  # Get today's date
    schedule = []

    # Daily tasks with fixed times
    for start_time, duration, task_name in daily_tasks:
        start_dt = datetime.combine(today_date, datetime.strptime(start_time, '%H%M').time())
        end_dt = start_dt + timedelta(minutes=duration)
        schedule.append((start_dt, end_dt, task_name))

    # Variable-time tasks
    for duration, task_name in variable_tasks:
        start_time = preferences.get(task_name, "Not Set")
        if start_time != "Not Set":
            start_dt = datetime.combine(today_date, datetime.strptime(start_time, '%H%M').time())
            end_dt = start_dt + timedelta(minutes=duration)
            schedule.append((start_dt, end_dt, task_name))

    # Conditional tasks based on the day of the week
    if str(day_of_week) in conditional_tasks:
        for start_time, duration, task_name in conditional_tasks[str(day_of_week)]:
            start_dt = datetime.combine(today_date, datetime.strptime(start_time, '%H%M').time())
            end_dt = start_dt + timedelta(minutes=duration)
            schedule.append((start_dt, end_dt, task_name))

    schedule.sort(key=lambda x: x[0])  # Sorts by start time
    return schedule

