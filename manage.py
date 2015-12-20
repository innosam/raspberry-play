import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask.ext.script import Manager
from raspberry_play import app
from controller import server

manager = Manager(app)

manager.add_command("runserver", server.Server())

if __name__ == "__main__":
    manager.run()
