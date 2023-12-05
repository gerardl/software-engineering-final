from models import User

class Authentication:
    def __init__(self, user_file):
        self.file_path = user_file
        self.users = self.__load_user_data()

    def __load_user_data(self):
        users = []
        with open(self.file_path, newline='') as file:
            for line in file:
                username, password = line.strip().split(', ')
                users.append(User(username, password))
        return users

    def login(self, username, password) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False
        