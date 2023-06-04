#author wlk
#date: 2023-06-04-11-05
import sys
reload(sys) 
sys.setdefaultencoding("utf-8")

import math
import requests
import yaml
import json
import os
import logging
import re
from logging.handlers import TimedRotatingFileHandler
import rospy
import datetime

loggerformat=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
filehandler=TimedRotatingFileHandler("/root/.ros/offset_path.log",when="S",interval=3600,backupCount=50)
filehandler.setFormatter(loggerformat)
logger=logging.getLogger("offset_path_check")
logger.addHandler(filehandler)
logger.setLevel(logging.INFO)
yamlfilepath="/root/launch/param/strategy.yaml"
check_dic={"0.06":11,"0.08":9,"0.1":7,"0.2":4} 
key_list=check_dic.keys()
starttime = datetime.datetime.now()
class MapID(object):
#get mapid and mapname 
#type :dict
    def GetCurrentMapIDInfo(self):
        url=" http://10.7.5.88:8080/gs-robot/real_time_data/robot_status"
        params={"sumary_info":1}
        try:
            response=requests.get(url=url,params=params,timeout=10)
        except Exception as ec:
            print("error={}".format(ec))
            logger.info("connect err={}".format(ec))
            return
        if response.status_code==200:
            logger.info("response:{} url={}".format(response.text,url))
            return response.text
        else:
            return 

    def GetElementValueFromJson(self,json,element_key):
        for element in json:
            if element_key==element:
                return json[element]

    def GetMapInfoFromCurrentMap(self,GetCurrentMapIDInfo):
        self.map_info={}
        if GetCurrentMapIDInfo is None:
            return False
        data=GetCurrentMapIDInfo
        logger.info("mapinfo={}".format(data))
        data=str(data)
        if isinstance(data,str):
            Str2data=json.loads(data)
            element_value_data=self.GetElementValueFromJson(Str2data,"data")
            logger.info("element_value={}".format(element_value_data))
            if element_value_data is not None:
                element_value_robotStatus=self.GetElementValueFromJson(element_value_data,"robotStatus")
                logger.info("element_value_robotStatus={}".format(element_value_robotStatus))
                if element_value_robotStatus is not None:
                    element_value_map=self.GetElementValueFromJson(element_value_robotStatus,"map")
                    logger.info("element_value_map={}".format(element_value_map))
                    if element_value_map is not None:
                        element_value_id=self.GetElementValueFromJson(element_value_map,"id")
                        logger.info("element_value_id={}".format(element_value_id))
                        self.map_info["mapid"]=element_value_id
                    else:
                        logger.info("not find data:robotStatus:map")
                        return
                    if element_value_map is not None:
                        element_value_name=self.GetElementValueFromJson(element_value_map,"name")
                        logger.info("element_value_id={}".format(element_value_id))
                        self.map_info["mapname"]=element_value_name
                    else:
                        logger.info("not find data:robotStatus:name")
                        return
                else:
                    logger.info("not find data:robotStatus")
                    return
            else:
                logger.info("not find data")
                return
        else:
            return
        return self.map_info  
class GetOfflineInfo(object):
    #get all csv_id,s filename ,for dectation xx_d.csv,
    def __init__(self,mapname):
        self.mapname=mapname
    def GetPathsInfo(self,mapname):
        old_url=" http://10.7.5.88:8080/gs-robot/data/paths"
        params={"map_name":mapname}
        try:
            response=requests.get(url=old_url,params=params,timeout=10)
        except Exception as ec:
            print("error={}".format(ec))
            logger.info("connect err={}".format(ec))
            return
        if response.status_code==200:
            logger.info("response:{} url={}".format(response.text,old_url))
            return response.text
    def GetOfflinePathsInfo(self,mapname):
        logger.info("map_name:{}".format(mapname))
        url=" http://10.7.5.88:8080/gs-robot/data/offline_paths"
        params={"map_name":mapname}
        try:
            response=requests.get(url=url,params=params,timeout=10)
        except Exception as ec:
            print("error={}".format(ec))
            logger.info("connect err={}".format(ec))
            return
        if response.status_code==200:
            logger.info("response:{} url={}".format(response.text,url))
            logger.info("new_url_path")
            return response.text
        else:
            return 
    def GetElementValueFromJson(self,json,element_key):
        for element in json:
            if element_key==element:
                return json[element]
            
    def GetPNCOfflineId(self,GetOfflinePathsInfo_):
        offlinepath_csvfilename=[]
        if GetOfflinePathsInfo_ is None:
            return
        data=GetOfflinePathsInfo_
        logger.info("mapinfo={}".format(data))
        data=str(data)
        if isinstance(data,str):
            Str2data=json.loads(data)
            element_value_data=self.GetElementValueFromJson(Str2data,"data")
            logger.info("element_value={}".format(element_value_data))
            if element_value_data is not None:
                if len(element_value_data)<1:
                    return
                for i in range(len(element_value_data)): 
                    if element_value_data[i]["type"]==1 or element_value_data[i]["type"]==7:
                        fileName=element_value_data[i]["fileName"]
                        if fileName is not None:
                            csvfilename=os.path.splitext(fileName)[0]
                            logger.info("offline_path_csv_id={}".format(csvfilename))
                            offlinepath_csvfilename.append(csvfilename)
                        else:
                            continue
                    else:
                        continue 
        else:
            return
        return offlinepath_csvfilename
    def GetPNClineId(self,GetPathsInfo_):
        path_csvfilename=[]
        if GetPathsInfo_ is None:
            return
        data=GetPathsInfo_
        logger.info("mapinfo={}".format(data))
        data=str(data)
        if isinstance(data,str):
            Str2data=json.loads(data)
            element_value_data=self.GetElementValueFromJson(Str2data,"data")
            logger.info("element_value={}".format(element_value_data))
            if element_value_data is not None:
                if len(element_value_data)<1:
                    return
                for i in  range(len(element_value_data)):
                    if element_value_data[i]["type"]==1 or element_value_data[i]["type"]==7:
                        fileName=element_value_data[i]["fileName"]
                        if fileName is not None:
                            csvfilename=os.path.splitext(fileName)[0]
                            logger.info("pnc_csv_id={}".format(csvfilename))
                            path_csvfilename.append(csvfilename)
                        else:
                            continue
                    else:
                        continue
        else:
            return
        return path_csvfilename 

class GetOffsetPathAndOffPathSwitch(object):
    offsetpath_dic={}
    def LoadDefaultParam(self):
        try:
            with open(yamlfilepath) as fd:
                strategydata=yaml.safe_load(fd)
                logger.info("load yaml successed data:{} path:{}".format(strategydata,yamlfilepath))
        except Exception as ec:
            logger.info("load yaml error={}".format(ec))
            return
        for node in strategydata:
            if node=="strategy":
                if "path_recorder" in strategydata[node]:
                    if "offset_switch" in strategydata[node]["path_recorder"]:
                        self.offsetpath_dic["offset_switch"]=strategydata[node]["path_recorder"]["offset_switch"]
                    if "offset_path" in strategydata[node]["path_recorder"]:
                         self.offsetpath_dic["offset_path"]=strategydata[node]["path_recorder"]["offset_path"]
                    logger.info("get offset data={}".format(self.offsetpath_dic))
                    return self.offsetpath_dic
    def getoffsetpathparam(self,LoadDefaultParam):
        offset_from_app={}
        rospy.init_node("get_offset_path_param")
        offset_switch=rospy.get_param("/strategy/path_recorder/offset_switch",LoadDefaultParam["offset_switch"])
        offset_path=rospy.get_param("/strategy/path_recorder/offset_path",LoadDefaultParam["offset_path"])
        offset_from_app["offset_switch"]=offset_switch
        offset_from_app["offset_path"]=offset_path
        if str(offset_from_app["offset_path"]) not in key_list:
            check_dic[str(offset_from_app["offset_path"])]=math.ceil(0.65/(float(offset_from_app["offset_path"])))
        logger.info("offset_param_from_app={}".format(offset_from_app))
        return offset_from_app
    


MapInfo=MapID()
GetCurrentMapIDInfo_=MapInfo.GetCurrentMapIDInfo()
mapinfo=MapInfo.GetMapInfoFromCurrentMap(GetCurrentMapIDInfo_)
mapname=mapinfo["mapname"]
mapid=mapinfo["mapid"]
GetOffLineInfo=GetOfflineInfo(mapname)

GetPathsInfo_=GetOffLineInfo.GetPathsInfo(mapname)
GetOfflinePathsInfo_=GetOffLineInfo.GetOfflinePathsInfo(mapname)
GetPNCOfflineId_=GetOffLineInfo.GetPNCOfflineId(GetOfflinePathsInfo_)
GetPNClineId_=GetOffLineInfo.GetPNClineId(GetPathsInfo_)
# print("GetPNCOfflineId_={}\nGetPNClineId_={}\n".format(GetPNCOfflineId_,GetPNClineId_))
GetOffsetPathAndOffPathSwitch_oj=GetOffsetPathAndOffPathSwitch()
LoadDefaultParam_=GetOffsetPathAndOffPathSwitch_oj.LoadDefaultParam()
getoffsetpathparam_=GetOffsetPathAndOffPathSwitch_oj.getoffsetpathparam(LoadDefaultParam_)
get_offset_switch=getoffsetpathparam_["offset_switch"]
get_offset_path=getoffsetpathparam_["offset_path"]
print("\n")
print("getoffsetpathparam={}\n".format(getoffsetpathparam_))
print("current_map_name={} current_mapid={}\n".format(mapname,mapid))
print("\n")
#up params would need 
csv_path="/root/GAUSSIAN_RUNTIME_DIR/map/"+mapid+"/path"
print("offset_path_dir: {}\n".format(csv_path)) 
print("Shold have {} path\n".format(check_dic[str(get_offset_path)]))
class GenerateCompletePaths(object):
    def __init__(self,path,offset,getpath_pncid_list) :
        self.path=path  
        self.offset=offset
        self.getpathpncid_list=getpath_pncid_list
    def get_file_path(self):
        return os.listdir(self.path)
    def reg_match_dict_offline_path_dir(self,get_file_path):
        ret_match_offline_path={}
        logger.info("getpath_pncid_list={}".format(self.getpathpncid_list))
        if self.getpathpncid_list is not None:
            index=0
            for paths_id in self.getpathpncid_list:
                paths_id_num=0
                index+=1
                logger.info("match_element={}".format(paths_id))
                for matched_csv_name in get_file_path:
                    regmatch=paths_id+"_[0-9]{1,2}\.csv$"
                    ret=re.match(regmatch,matched_csv_name)
                    if ret:
                        logger.info("matched:{}".format(matched_csv_name))
                        paths_id_num+=1
                    else:
                        logger.info("canot match:{}".format(matched_csv_name))
                        continue
                ret_match_offline_path[paths_id]=paths_id_num
                if index==len(self.getpathpncid_list):
                    return ret_match_offline_path
            return ret_match_offline_path
        else:
            return ret_match_offline_path
    def get_offline_raw_path_dir(self,get_file_path):
        ret_matched_offline_raw_dir={}
        if self.getpathpncid_list:
            for paths_id in self.getpathpncid_list:
                raw_path_num=0
                raw_path=paths_id+".csv"
                if raw_path in get_file_path:
                    raw_path_num+=1
                ret_matched_offline_raw_dir[paths_id]=raw_path_num
        return ret_matched_offline_raw_dir

    def ret_raw_offset_path_dir(self,reg_match_dict_offline_path_dir,get_offline_raw_path_dir): 
        ret_real_offset_dir={}
        if self.getpathpncid_list:
            for paths_done in self.getpathpncid_list:
                ret_real_offset_dir[paths_done]=reg_match_dict_offline_path_dir[paths_done]+get_offline_raw_path_dir[paths_done]
        return ret_real_offset_dir
    def real_offset_path_done(self,ret_raw_offset_path_dir):
        should_done_real_done={}
        should_done_num=0
        if self.getpathpncid_list:
            should_done_num=len(self.getpathpncid_list)
        sholud_done_offset_path=check_dic[str(self.offset)]
        
        real_done_num=0
        ret_offline_path_dir_keys=ret_raw_offset_path_dir.keys()
        for elem in ret_offline_path_dir_keys:
            if sholud_done_offset_path<=ret_raw_offset_path_dir[elem]:
                real_done_num+=1
            else:
                # print("\033[0;31;40mfailed filename={}\033[0m".format(elem))
                pass
        should_done_real_done["should_done_num"]=should_done_num
        should_done_real_done["real_done_num"]=real_done_num
        return should_done_real_done
    def ret_failed_list(self,ret_raw_offset_path_dir):
        failed_file_name_list=[]
        sholud_done_offset_path=check_dic[str(self.offset)]
        ret_offline_path_dir_keys=ret_raw_offset_path_dir.keys()
        for elem in ret_offline_path_dir_keys:
            if sholud_done_offset_path<=ret_raw_offset_path_dir[elem]:
                pass
            else:
                failed_file_name_list.append(elem)
        return failed_file_name_list
    def ret_successed_list(self,ret_raw_offset_path_dir):
        successed_file_name_list=[]
        sholud_done_offset_path=check_dic[str(self.offset)]
        ret_offline_path_dir_keys=ret_raw_offset_path_dir.keys()
        for elem in ret_offline_path_dir_keys:
            if sholud_done_offset_path<=ret_raw_offset_path_dir[elem]:
                successed_file_name_list.append(elem)
        return successed_file_name_list
    
#common param

#offset_path
GenerateCompletePaths_oj_offsetpath=GenerateCompletePaths(path=csv_path, offset=get_offset_path, getpath_pncid_list=GetPNCOfflineId_)
get_file_path_=GenerateCompletePaths_oj_offsetpath.get_file_path()
reg_match_dict_offline_path_dir_=GenerateCompletePaths_oj_offsetpath.reg_match_dict_offline_path_dir(get_file_path_)
get_offline_raw_path_dir_=GenerateCompletePaths_oj_offsetpath.get_offline_raw_path_dir(get_file_path_)
ret_raw_offset_path_dir_=GenerateCompletePaths_oj_offsetpath.ret_raw_offset_path_dir(reg_match_dict_offline_path_dir_,get_offline_raw_path_dir_)
real_offset_path_done_=GenerateCompletePaths_oj_offsetpath.real_offset_path_done(ret_raw_offset_path_dir_)
ret_failed_list_offsetpath_=GenerateCompletePaths_oj_offsetpath.ret_failed_list(ret_raw_offset_path_dir_)
ret_successed_list_offsetpath_=GenerateCompletePaths_oj_offsetpath.ret_successed_list(ret_raw_offset_path_dir_)

#path
GenerateCompletePaths_oj_offsetpath=GenerateCompletePaths(path=csv_path, offset=get_offset_path, getpath_pncid_list=GetPNClineId_)
# get_file_path_=GenerateCompletePaths_oj_offsetpath.get_file_path()
reg_match_dict_path_dir_=GenerateCompletePaths_oj_offsetpath.reg_match_dict_offline_path_dir(get_file_path_)
get_path_raw_path_dir_=GenerateCompletePaths_oj_offsetpath.get_offline_raw_path_dir(get_file_path_)
ret_raw_path_dir_=GenerateCompletePaths_oj_offsetpath.ret_raw_offset_path_dir(reg_match_dict_path_dir_,get_path_raw_path_dir_)
real_path_path_done_=GenerateCompletePaths_oj_offsetpath.real_offset_path_done(ret_raw_path_dir_)
ret_failed_list_path_=GenerateCompletePaths_oj_offsetpath.ret_failed_list(ret_raw_path_dir_)
ret_successed_list_path_=GenerateCompletePaths_oj_offsetpath.ret_successed_list(ret_raw_path_dir_)

def dispaly_successed_list(list):
    if list:
        for elem in list:
            print("\033[0;32;40msuccessed filename={}\033[0m".format(elem))

def dispaly_failed_list(list):
    if list:
        for elem in list:
            print("\033[0;31;40mfailed filename={}\033[0m".format(elem))

def run_main():
    if get_offset_switch:
        print("------------------------------>offset_paths<------------------------------\n")
        print("\033[0;33;40m{}\033[0m\n".format(real_offset_path_done_))
        print("getoffline_path_failed_filename_list:\n")
        dispaly_failed_list(ret_failed_list_offsetpath_)
        print("\n")
        print("getoffline_path_successed_filename_list:\n")
        dispaly_successed_list(ret_successed_list_offsetpath_)
        print("\n")
        if real_offset_path_done_["should_done_num"]==real_offset_path_done_["real_done_num"]:
            print("offline_paths_complete_done:\033[0;31;40m{}\033[0m\n".format(True))
        else:
            print("offline_paths_complete_done:\033[0;31;40m{}\033[0m\n".format(False))
        # print("raw_dir_list={}".format(getofflinecompleted_object.ret_raw_offset_path_dir())) #test using 
        print("\n")
        print("--------------------------------->paths<---------------------------------\n")
        print("\033[0;33;40m{}\033[0m\n".format(real_path_path_done_))
        print("getpath_failed_filename_list:\n")
        dispaly_failed_list(ret_failed_list_path_)
        print("\n")
        print("getpath_successed_filename_list:\n")
        dispaly_successed_list(ret_successed_list_path_)
        print("\n")
        if real_path_path_done_["should_done_num"]==real_path_path_done_["real_done_num"]:
            print("paths_complete_done: \033[0;31;40m{}\033[0m\n".format(True))
        else:
            print("paths_complete_done: \033[0;31;40m{}\033[0m\n".format(False))
    else:
        print("\n")
        print("\033[0;32;40moffset_switch :{} please open it\033[0m\n".format(get_offset_switch))

if __name__=="__main__":
    run_main()
    endtime = datetime.datetime.now()
    print("used_time={}Ms".format(int((endtime-starttime).microseconds)/1000))
  