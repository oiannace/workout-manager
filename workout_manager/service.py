from models import (userModel, exerciseModel)


class exerciseService:
    def __init__(self):
        self.model = exerciseModel()

    def create(self, params):
        return self.model.create(params)

    def update(self, item_id, params):
        return self.model.update(item_id, params)

    def delete(self, item_id):
        return self.model.delete(item_id)

    def list(self):
        response = self.model.list_items()
        return response
    
    def get_by_id(self, item_id):
        response = self.model.get_by_id(item_id)
        return response

class userService:
    def __init__(self):
        self.model = userModel()

    def register(self, params):
        return self.model.register(params)

    def login(self, params):
        return self.model.login(params)