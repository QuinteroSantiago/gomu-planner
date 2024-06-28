import json

class Config:
    def __init__(self, tasks_file='tasks_data.json'):
        self.tasks_file = tasks_file
        self.tasks_data = self.load_data()
        self.preferences = self.tasks_data.get('preferred_times', {})
        self.daily_tasks = self.tasks_data.get('daily_tasks', [])
        self.variable_tasks = self.tasks_data.get('variable_tasks', [])
        self.conditional_tasks = self.tasks_data.get('conditional_tasks', {})

    def load_data(self):
        """ Load data from a JSON file. """
        try:
            with open(self.tasks_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}  # Return an empty dict if no file exists

    def save_data(self, data):
        """ Save data to a JSON file. """
        with open(self.tasks_file, 'w') as file:
            json.dump(data, file, indent=4)

    def update_preferences(self, task_name, new_time):
        """ Update the preferences in the configuration and save to file. """
        self.preferences[task_name] = new_time
        self.save_data(self.tasks_data)
