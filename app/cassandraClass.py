from cassandra.cluster import Cluster
from app import app
import json

class Cassandra:
    def __init__(self):
        self.id = None
        self.data = None
        self.cluster = None
        self.session = None
        self.server = None
        self.port = None
        app.config.from_object('config.ProductionConfig')
    #This methd to connectto cassandra database
    @staticmethod
    def cassandraConnection(self):
        self.server = app.config["SERVER_NAME_DB"]
        self.port = app.config["PORT_DB"]
        self.cluster = Cluster([self.server], port=self.port)
        self.session = self.cluster.connect()
        self.session.execute("""
            CREATE KEYSPACE IF NOT EXISTS forexhistory
            WITH REPLICATION =
            { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
            """)
        self.session.set_keyspace('forexhistory')
        return self.session, self.cluster

    #This method is tocreate forexhistory table
    def createForexHistoryTable(self):
        #self.cassandraConnection()
        c_sql = """
                       CREATE TABLE IF NOT EXISTS forexhistory (datedon text,
                                                           basecurrency text,
                                                           targetcurrency text,
                                                           rate float,
                                                           PRIMARY KEY (datedon, basecurrency, targetcurrency)                                                        
                                                            ) WITH CLUSTERING ORDER BY (basecurrency asc,targetcurrency asc);
                 """
        self.session.execute(c_sql)

    def isTableEmpty(self):
        c_sql = """ SELECT count(*) FROM forexhistory """
        rows = self.session.execute(c_sql)
        for row in rows:
            if row.count ==0:
                self.insertAllData(True)
            else:
                return False

    def insertAllData(self, isEmpty):
        if isEmpty==True:
            c_sql = """ SELECT count(*) FROM forexhistory """

    #This method helps to insertdata int DB
    def insertForexHistoryData(self, datedOn, baseCurr, targetCurr, rate):
        self.datedOn = datedOn
        self.baseCurr = baseCurr
        self.targetCurr = targetCurr
        self.rate = rate
        #self.cassandraConnection()
        query = "INSERT INTO forexhistory (datedOn, baseCurrency, targetCurrency, rate) VALUES (%s, %s, %s, %s)"
        self.session.execute(query, (self.datedOn, self.baseCurr, self.targetCurr,  self.rate))

    #This method gets the lastupdated Date in DB
    def selectLastUpdatedDate(self):
        query = "SELECT MAX(datedOn) as lastupdated FROM forexhistory;"
        values = self.session.execute(query)
        if not values:
            lastUpdatedDate = None
        else:
            lastUpdatedDate = values[0].lastupdated
        return lastUpdatedDate

    def selectForexHistoryDay(self, date, base, target):
        #self.cassandraConnection()
        cql_dict = []
        cql_dict = dict.fromkeys(['date', 'base', 'target', 'rate'])
        query = "SELECT * FROM forexhistory where datedon='{0}' AND basecurrency='{1}' AND targetcurrency='{2}';".format(date,
                                                                                                                base,
                                                                                                                target)
        rows = self.session.execute(query)
        dateList = []
        rateList = []
        baseList = []
        targetList = []
        for row in rows:
            dateList.append(row.datedon)
            baseList.append(row.basecurrency)
            targetList.append(row.targetcurrency)
            rateList.append(row.rate)
        dictionary = [{"date": d, "base": b, "target": t, "rate": r} for d, b, t, r in
                      zip(dateList, baseList, targetList, rateList)]
        return json.dumps(dictionary)

    def selectForexHistoryTimeframe(self, startdate, enddate, basecurr, tarcurr):
        #self.cassandraConnection()
        dateList = []
        rateList = []
        baseList = []
        targetList = []
        query = "select * from forexhistory where datedon >= '{0}' and datedon <= '{1}' AND basecurrency='{2}' and targetcurrency='{3}' ALLOW FILTERING;".format(startdate, enddate, basecurr, tarcurr)
        rows = self.session.execute(query)
        for row in rows:
            dateList.append(row.datedon)
            baseList.append(row.basecurrency)
            targetList.append(row.targetcurrency)
            rateList.append(row.rate)
        dictionary = [{"date": d, "base": b, "target": t, "rate": r} for d, b, t, r in zip(dateList, baseList, targetList, rateList)]
        return json.dumps(dictionary)

    def createLoginTable(self):
        #self.cassandraConnection()
        c_sql = """
                               CREATE TABLE IF NOT EXISTS forexlogin (username text,
                                                                   userid text,
                                                                   email text,
                                                                   password text,
                                                                   PRIMARY KEY (email)                                                        
                                                                    );
                         """
        self.session.execute(c_sql)

    def insertUsers(self, username, userid, email, password):
        #self.cassandraConnection()
        c_sql = "INSERT INTO forexlogin (username, userid, email, password) VALUES ('{0}', '{1}', '{2}','{3}');"
        self.session.execute(c_sql, self.username, self.userid, self.email, self.password)

    def getCredentials(self, email):
        #self.cassandraConnection()
        c_sql = "SELECT password from forexlogin WHERE email='{0}');"
        values = self.session.execute(c_sql, self.email)
        if not values:
            password = None
        else:
            password = values[0].password
        return password