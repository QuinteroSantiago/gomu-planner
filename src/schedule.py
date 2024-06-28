from datetime import datetime, timedelta, date

def create_schedule(daily_tasks, variable_tasks, day_of_week, preferences):
    today_date = date.today()
    schedule = []

    for task in daily_tasks:
        start_dt = datetime.combine(today_date, task.start_time)
        end_dt = start_dt + timedelta(minutes=task.duration)
        schedule.append((start_dt, end_dt, task.task_name))

    for task in variable_tasks:
        start_time = preferences.get(task.task_name)
        if start_time:
            start_dt = datetime.combine(today_date, start_time)
            end_dt = start_dt + timedelta(minutes=task.duration)
            schedule.append((start_dt, end_dt, task.task_name))

    schedule.sort(key=lambda x: x[0])
    return schedule
