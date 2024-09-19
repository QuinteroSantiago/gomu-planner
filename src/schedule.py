from datetime import datetime, timedelta, date
from .db.models import Frequency

def create_schedule(tasks, day_of_week, preferences):
    today_date = date.today()
    schedule = []
    for task in tasks:
        if task.frequency == Frequency.WEEKLY and task.day_of_week != day_of_week:
            continue
        if task.frequency == Frequency.MONTHLY and task.day_of_month != today_date.day:
            continue
        if task.frequency == Frequency.YEARLY and task.specific_date is not None and (task.specific_date.day != today_date.day or task.specific_date.month != today_date.month):
            continue
        start_time = preferences.get(task.task_name)
        if start_time:
            start_dt = datetime.combine(today_date, start_time)
            end_dt = start_dt + timedelta(minutes=task.duration)
            category_name = task.category.category_name if task.category else "None"
            task_duration = task.duration
            schedule.append((start_dt, end_dt, task.task_name, category_name, task_duration))

    schedule.sort(key=lambda x: x[0])
    return schedule
