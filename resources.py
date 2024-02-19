resources = ["gamemenu"]

def load_all_resources():
    for r in resources:
        __import__(r).load_resources()