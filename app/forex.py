from app.cassandraClass import Cassandra
from app.forexInitialize import ForexInitializationClass
from app import app
from flask.views import View


def forexInitializeMethod():
    # obj1 = Cassandra()
    # obj1.cassandraConnection()
    # obj1.createForexHistoryTable()
    Obj2 = ForexInitializationClass()
    Obj2.forexClassNavigator()


@app.route('/test')
def hello():
    return 'hello'


class ForexHistory(View, ForexInitializationClass):

    def dispatch_request(self, startdate, basecurr, tarcurr):
        return self.cassandraObj.selectForexHistoryDay(startdate, basecurr, tarcurr)


forexHistoryview = ForexHistory.as_view('forexHistory')
app.add_url_rule('/history/<startdate>/<basecurr>/<tarcurr>', view_func=forexHistoryview)


class ForexHistoryimeframe(View, ForexInitializationClass):
    def dispatch_request(self, startdate, enddate, basecurr, tarcurr):
        return self.cassandraObj.selectForexHistoryTimeframe(startdate, enddate, basecurr, tarcurr)

forexHistoryTimeframeview = ForexHistoryimeframe.as_view('forexHistoryTimeframe')
app.add_url_rule('/history/<startdate>/<enddate>/<basecurr>/<tarcurr>', view_func=forexHistoryTimeframeview)