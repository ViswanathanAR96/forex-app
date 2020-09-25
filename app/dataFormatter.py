from app import app
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json


class DataFormatter:

    def __init__(self):
        self.today = None
        self.lastYearToday = None
        self.json = None

    def convertToDatetime(self, date):
        datetimeDate = datetime.date(datetime.strptime(str(date), '%Y-%m-%d'))
        return datetimeDate

    def getCurrentDate(self):
        weekday = datetime.date(datetime.now())
        return weekday

    def getRequiredDates(self):
        self.today = self.isWeekend(self.getCurrentDate())
        self.lastYearToday = self.isWeekend(self.today - relativedelta(years=1))
        return self.today, self.lastYearToday

    def isWeekend(self, date):
        if date.weekday() == 5:
            date = date - relativedelta(days=1)
        elif date.weekday() == 6:
            date = date - relativedelta(days=2)
        return date

    def isWeekend2(self, date):
        if date.weekday() == 5:
            date = date + relativedelta(days=2)
        elif date.weekday() == 6:
            date = date + relativedelta(days=1)
        return date

    def noOfDaysBtwDates(self, firstDate, lastDate):
        noOfDays = lastDate - firstDate
        return noOfDays.days

    def addADay(self, lastUpdatedDate):
        #If the lastupdated day is a friday or saturday, then update the nextday to monday, else add one day.
        if lastUpdatedDate.weekday() == 4:
            lastUpdatedDate = lastUpdatedDate + relativedelta(days=3)
        elif lastUpdatedDate.weekday() == 5:
            lastUpdatedDate = lastUpdatedDate + relativedelta(days=2)
        else:
            lastUpdatedDate = lastUpdatedDate + relativedelta(days=1)
        return lastUpdatedDate


