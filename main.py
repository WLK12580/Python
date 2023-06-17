# #!/usr/bin/python
# #-*-coding:utf-8 -*-
# import pymysql #导入模块

# #远程连接数据库
# try:
#     db = pymysql.connect(
#             host='192.168.0.108',
#             port=3306,
#             user='root',
#             passwd='erjk',
#             db='mydatabase',
#             charset='utf8'
#             )
#     print("successed")
# except:
#     print('something wrong!')

# #使用cursor()方法获取操作游标 
# cursor = db.cursor()
# cursor.execute("SELECT VERSION()")
# data = cursor.fetchone()
# print("Database version : %s " % data)



# list=[1,2,3]
# del list[1]
# print(list[1])
import time
from logger_package.logger import Logger
def main(): 
    logger=Logger() #
    int_sum=0
    logger.set_log_name("tar_gz")
    while True:
        int_sum+=1
        logger.info("logger",int_sum)
        logger.debug("debug","test")
        logger.warning("warning","hello")
        logger.error("error","error")
        logger.critical("critical_","critical")
        time.sleep(3)
if __name__=="__main__":
    main()
        