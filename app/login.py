from flask_bcrypt import Bcrypt
from app import app
from flask.views import View

@app.route('/login/<username>/<password>')
def login(self, username, password):
    return self.cassandraObj.selectForexHistoryDay(startdate, basecurr, tarcurr)

@app.route('/register', method=['POST'])
def register()


