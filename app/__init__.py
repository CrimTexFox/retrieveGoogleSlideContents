import logging
from flask import Flask

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

from app import main
