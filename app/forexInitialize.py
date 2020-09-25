from app import app
import requests
from app.cassandraClass import Cassandra
from app.dataFormatter import DataFormatter


class ForexInitializationClass():

    def __init__(self):
        self.api_key = None
        self.startDate = None
        self.endDate = None
        self.cassandraObj = Cassandra()
        self.dateobj = None

    #This method is to connect to the fxmarketAPI to get data between te given initial dates
    def fxForexApi(self, fromDate, toDate):
        self.api_key = app.config["FX_API_KEY"]
        self.startDate = fromDate
        self.endDate = toDate
        self.cassandraObj.cassandraConnection()
        r = requests.get(
            """https://fxmarketapi.com/apitimeseries?api_key={0}&currency=USDEUR,USDGBP,USDCAD,USDCHF,USDAUD,USDJPY,CADEUR,CADGBP,CADCHF,CADAUD,CADJPY,CADUSD,CHFEUR,CHFGBP,CHFCAD,CHFAUD,CHFJPY,CHFUSD,AUDEUR,AUDGBP,AUDCAD,AUDCHF,AUDJPY,AUDUSD,JPYEUR,JPYGBP,JPYCAD,JPYCHF,JPYAUD,JPYUSD,EURUSD,EURGBP,EURCAD,EURCHF,EURAUD,EURJPY,GBPUSD,GBPUSD,GBPCAD,GBPCHF,GBPAUD,GBPJPY&start_date={1}&end_date={2}&format=close""".format(
                self.api_key, self.startDate, self.endDate))
        data = r.json()
        return data

    #This method insers the data fetched by GET methods into DB
    def insertDataIntoDb(self, data):
        for key, value in data["price"].items():
            for key2, value2 in value.items():
                baseCurr = key2[0:3]
                targetCurr = key2[3:6]
                self.cassandraObj.insertForexHistoryData(key, baseCurr, targetCurr, value2)

    #This method gets data of the past 1 year
    def getForexOneYearData(self):
        self.api_key = app.config["FX_API_KEY"]
        self.endDate, self.startDate = self.dateobj.getRequiredDates()
        self.cassandraObj.createForexHistoryTable()
        jsonBlob = self.fxForexApi(self.startDate, self.endDate)
        self.insertDataIntoDb(jsonBlob)

    #This method stores data that are missing between today and lastupdatedDate
    def getMissedDatesData(self, lastUpdate):
        lastUpdatedDate = self.dateobj.convertToDatetime(lastUpdate)
        today = self.dateobj.getCurrentDate()
        #Adding one day from the last updatedDate to fetch records from next day
        lastUpdatedDateTemp = self.dateobj.addADay(lastUpdatedDate)
        todayTemp = self.dateobj.isWeekend(today)
        noOfDays = self.dateobj.noOfDaysBtwDates(lastUpdatedDateTemp, todayTemp)
        if noOfDays >= 0:
           missedDataJsonBlob = self.fxForexApi(lastUpdatedDateTemp, todayTemp)
           self.insertDataIntoDb(missedDataJsonBlob)

    #This method decides whether to get results of past 1 year or only for the missing days
    def forexClassNavigator(self):
        self.cassandraObj.cassandraConnection()
        self.dateobj = DataFormatter()
        print(self.cassandraObj.selectLastUpdatedDate())
        lastUpdatedDate = self.cassandraObj.selectLastUpdatedDate()
        if lastUpdatedDate is None:
            self.getForexOneYearData()
        elif self.dateobj.convertToDatetime(lastUpdatedDate) <= self.dateobj.getCurrentDate():
            self.getMissedDatesData(lastUpdatedDate)
