
import time
import os
from datetime import datetime
class Logger(object):
    current_hour=0
    log_filename_=""
    logname_list=[] #
    loghour_list=[]
    log_tag_name=""
    log_filename=""
    internal_time=3600
    def __init__(self):
        self.current_hour=self._get_current_hour()
        self.log_filename_=self._get_current_date()+".log"
    def _get_current_hour(self):
        current_hour=int(time.time()/(self.internal_time))
        if current_hour not in self.loghour_list:   
            self.loghour_list.append(current_hour)
        return current_hour
    def _get_current_date(self): #
        current_stamp=self.current_hour*(self.internal_time)
        date_data=datetime.fromtimestamp(current_stamp)
        date_format=date_data.strftime("%Y-%m-%d-%H-%M-%S")
        return date_format
    def set_log_name(self,logname):
        self.current_hour=self._get_current_hour()
        self.log_filename_=self._get_current_date()+".log"
        self.log_filename=logname+"_"+self.log_filename_
        self.creat_logfile()
        self.log_tag_name=logname
        return self.log_filename
    def creat_logfile(self):
        if not os.path.exists(self.log_filename):
            os.mknod(self.log_filename)
        else:
            pass
        if self.log_filename not in self.logname_list:
            self.logname_list.append(self.log_filename)
        return self.logname_list
    
    def info(self,message):
        if(int(time.time()/(self.internal_time))-self.loghour_list[0]>=1) or not os.path.exists(self.log_filename):
            Logger()
            self.set_log_name(self.log_tag_name)
            self.creat_logfile()
            if len(self.loghour_list)>1:
                del self.loghour_list[0]
        file_name=""
        if len(self.logname_list)==1:
            file_name=self.logname_list[0]
        if len(self.logname_list)==2:
            file_name=self.logname_list[1]
            del self.logname_list[0]
        with open(file_name,"a+") as fd:
            fd.write("{0:<20} {1:<4} {2:<10}".format(str(datetime.now()).replace(" ","-"),"INFO",message))
            fd.write("\n")
        fd.close()
    def warning(self,message):
        if(int(time.time()/(self.internal_time))-self.loghour_list[0]>=1) or not os.path.exists(self.log_filename):
            Logger()
            self.set_log_name(self.log_tag_name)
            self.creat_logfile()
            if len(self.loghour_list)>1:
                del self.loghour_list[0]
        file_name=""
        if len(self.logname_list)==1:
            file_name=self.logname_list[0]
        if len(self.logname_list)==2:
            file_name=self.logname_list[1]
            del self.logname_list[0]
        with open(file_name,"a+") as fd:
            fd.write("{0:<20} {1:<4} {2:<10}".format(str(datetime.now()).replace(" ","-"),"WARNNING",message))
            fd.write("\n")
        fd.close()
    def debug(self,message):
        if(int(time.time()/(self.internal_time))-self.loghour_list[0]>=1) or not os.path.exists(self.log_filename):
            Logger()
            self.set_log_name(self.log_tag_name)
            self.creat_logfile()
            if len(self.loghour_list)>1:
                del self.loghour_list[0]
        file_name=""
        if len(self.logname_list)==1:
            file_name=self.logname_list[0]
        if len(self.logname_list)==2:
            file_name=self.logname_list[1]
            del self.logname_list[0]
        with open(file_name,"a+") as fd:
            fd.write("{0:<20} {1:<4} {2:<10}".format(str(datetime.now()).replace(" ","-"),"DEBUG",message))
            fd.write("\n")
        fd.close()
    def critical(self,message):
        if(int(time.time()/(self.internal_time))-self.loghour_list[0]>=1) or not os.path.exists(self.log_filename):
            Logger()
            self.set_log_name(self.log_tag_name)
            self.creat_logfile()
            if len(self.loghour_list)>1:
                del self.loghour_list[0]
        file_name=""
        if len(self.logname_list)==1:
            file_name=self.logname_list[0]
        if len(self.logname_list)==2:
            file_name=self.logname_list[1]
            del self.logname_list[0]
        with open(file_name,"a+") as fd:
            fd.write("{0:<20} {1:<4} {2:<10}".format(str(datetime.now()).replace(" ","-"),"CRITICAL",message))
            fd.write("\n")
        fd.close()
    def error(self,message):
        if(int(time.time()/(self.internal_time))-self.loghour_list[0]>=1) or not os.path.exists(self.log_filename):
            Logger()
            self.set_log_name(self.log_tag_name)
            self.creat_logfile()
            if len(self.loghour_list)>1:
                del self.loghour_list[0]
        file_name=""
        if len(self.logname_list)==1:
            file_name=self.logname_list[0]
        if len(self.logname_list)==2:
            file_name=self.logname_list[1]
            del self.logname_list[0]
        with open(file_name,"a+") as fd:
            fd.write("{0:<20} {1:<4} {2:<10}".format(str(datetime.now()).replace(" ","-"),"ERROR",message))
            fd.write("\n")
        fd.close()
