#! /usr/bin/python3

import logging
import sys
import os 

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/dyue/flask_playground/')

from flask_playground import app as application
application.secret_key="FAKEKEYFORNOW"

#from dotenv import load_dotenv
#load_dotenv()
#application.secret_key = os.environ["SECRETKEY"]
