import json
import os

config_file = os.path.join(os.path.dirname(__file__), 'config.json')

class Configurations:
    def __init__(self):
        config = json.load(open(config_file))
        self.project_home = config['projectHome']
        self.log_folder = os.path.join(self.project_home, 'logs')
        self.image_upload_folder = os.path.join(self.project_home, 'image_uploads')
        self.logToFile = config['logToFile']