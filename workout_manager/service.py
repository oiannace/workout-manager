from models import (userModel, exerciseModel)


class exerciseService:
    def __init__(self):
        self.model = exerciseModel()

    def create(self, params):
        return self.model.create(params)

    def update(self, exercise_id, params):
        return self.model.update(exercise_id, params)

    def delete_by_id(self, exercise_id):
        return self.model.delete_by_id(exercise_id)

    def list(self):
        response = self.model.list_exercises()
        return response
    
    def get_by_id(self, exercise_id):
        response = self.model.get_by_id(exercise_id)
        return response

    def get_by_name(self, exercise_name):
        response = self.model.get_by_name(exercise_name)
        return response

class userService:
    def __init__(self):
        self.model = userModel()

    def register(self, params):
        return self.model.register(params)

    def login(self, params):
        return self.model.login(params)