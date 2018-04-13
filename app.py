from flask import Flask
from apis import api
# from werkzeug.contrib.fixers import ProxyFix
import logging
import os
from configurations import Configurations
from datetime import datetime

config = Configurations()
if not os.path.isdir(config.log_folder):
    os.makedirs(os.path.join(config.log_folder))

if not os.path.isdir(config.image_upload_folder):
    os.makedirs(os.path.join(config.image_upload_folder))

logging.getLogger(__file__)

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

logname = 'logs_{}.h5'.format(datetime.now().strftime('%Y-%m-%d--%H-%M-%S'))

if config.logToFile:
    logging.basicConfig(level=logging.DEBUG,
                        format=LOG_FORMAT,
                        filename=os.path.join(config.project_home, 'logs', logname))
else:
    logging.basicConfig(level=logging.DEBUG,
                        format=LOG_FORMAT)


app = Flask(__name__)

# app.wsgi_app = ProxyFix(app.wsgi_app)

api.init_app(app)

app.run(debug=False)