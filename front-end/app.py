from flask import Flask, send_from_directory, request
from flask import render_template
from flask import jsonify
import datetime
import pdb
import statistics
from operator import itemgetter
import numpy as np
import csv
import random
import requests
from os import path
from bs4 import BeautifulSoup
import os

from genie import genie

# os.environ["FLASK_ENV"] = "development"

app = Flask("genie")
app.register_blueprint(genie)

app.run(host = "0.0.0.0", port = os.environ["PORT"] || 5000)
