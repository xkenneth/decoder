import datetime

class smart_datetime(datetime.datetime):
    def __float__(self):
        return float(self.hour*60*60) + float(self.minute*60) + float(self.second) + float(self.microsecond/1000000.0)

class smart_timedelta(datetime.timedelta):
    def __float__(self):
        return float(self.seconds) + float(self.microseconds/1000000.0)
