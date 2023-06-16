# Python
import logging
import time
from datetime import datetime
import os
class Log(object):
    saves_time=0
    pre_hours=0
    fd=0
    def __init__(self):
    
        self.saves_time=self._get_current_hours()
        self.logname=self.saves_time+".log"
        self._create_log()
        self.pre_hours=int(time.time()/3600)
    
    def _get_current_hours(self):
        current_hours_date=int(time.time()/3600)*3600
        date_time=str(datetime.fromtimestamp(current_hours_date))
        date_time=date_time.replace(" ","-")
        date_time=date_time.replace(":", "-")
        logging.info(date_time)
        return date_time
    def _create_log(self):
        if not os.path.exists(self.logname):
            os.mknod(self.logname)
        return
    def _close_log(self):
        return self.fd.close()
            
    def info(self,anno,data):
        print("self.pre_hours={}".format(self.pre_hours))
        if(int(time.time()/3600)-self.pre_hours>=1) or not os.path.exists(self.logname):
            Log()
            self._create_log()
        if (int(time.time()/3600)-self.pre_hours>=1):
            self._close_log()
        with open(self.logname,"a+") as fd:
            print("using_log_name={}".format(self.logname))
            # line=str(datetime.now()).replace(" ","-")+" INFO"+" "+str(anno)+" "+str(data)
            fd.write("%-20s %-10s %-10s %s"%(str(datetime.now()).replace(" ","-"),"INFO",str(anno),data))
            # fd.write(line)
            fd.write("\n")
            fd.close()
    def warning(self,anno,data):
        if(int(time.time()/3600)-self.pre_hours>=1) or not os.path.exists(self.logname):
            Log()
            self._create_log()
        if (int(time.time()/3600)-self.pre_hours>=1):
            self._close_log()
        with open(self.logname,"a+") as self.fd:
            self.fd.write("%-20s %-10s %-10s %s"%(str(datetime.now()).replace(" ","-"),"WARNING",str(anno),data))
            self.fd.write("\n")
            self.fd.close()
    def error(self,anno,data):
        if(int(time.time()/3600)-self.pre_hours>=1) or not os.path.exists(self.logname):
            Log()
            self._create_log()
        if (int(time.time()/3600)-self.pre_hours>=1):
            self._close_log()
        with open(self.logname,"a+") as fd:
            # line=str(datetime.now()).replace(" ","-")+" ERROR"+" "+str(anno)+" "+str(data)
            fd.write("%-20s %-10s %-10s %s"%(str(datetime.now()).replace(" ","-"),"ERROR",str(anno),data))
            fd.write("\n")
            fd.close()
    def debug(self,anno,data):
        if(int(time.time()/3600)-self.pre_hours>=1) or not os.path.exists(self.logname):
            Log()
            self._create_log()
        if (int(time.time()/3600)-self.pre_hours>=1):
            self._close_log()
        with open(self.logname,"a+") as fd:
            fd.write("%-20s %-10s %-10s %s"%(str(datetime.now()).replace(" ","-"),"DEBUG",str(anno),data))
            # line=str(datetime.now()).replace(" ","-")+" DEBUG"+" "+str(anno)+" "+str(data)
            # fd.write(line)
            fd.write("\n")
            fd.close()
    def critical(self,anno,data):
        if(int(time.time()/3600)-self.pre_hours>=1) or not os.path.exists(self.logname):
            Log()
            self._create_log()
        if (int(time.time()/3600)-self.pre_hours>=1):
            self._close_log()
        with open(self.logname,"a+") as fd:
            # line=str(datetime.now()).replace(" ","-")+" CRITICAL"+" "+str(anno)+" "+str(data)
            fd.write("%-20s %-10s %-10s %s"%(str(datetime.now()).replace(" ","-"),"CRITICAL",str(anno),data))
            # fd.write(line)
            fd.write("\n")
            fd.close()
