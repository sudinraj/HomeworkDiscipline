import json

def addGame(game):
    with open("games.json", 'r+') as file:
        file_data = json.load(file)
        file_data["userList"].append(game)
        file.seek(0)
        json.dump(file_data, file)
    file.close()