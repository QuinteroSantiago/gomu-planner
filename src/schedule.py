from datetime import datetime, timedelta, date

def create_schedule(tasks, day_of_week, preferences):
    today_date = date.today()
    schedule = []
    # print(f'preferences: {preferences}')

    for task in tasks:
        start_time = preferences.get(task.task_name)
        if start_time:
            start_dt = datetime.combine(today_date, start_time)
            end_dt = start_dt + timedelta(minutes=task.duration)
            category_name = task.category.category_name if task.category else "None"
            schedule.append((start_dt, end_dt, task.task_name, category_name))

    schedule.sort(key=lambda x: x[0])
    return schedule
