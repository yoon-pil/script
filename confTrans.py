#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys, os, linecache
from datetime import datetime, timedelta 
from colorama import Fore
Pwd = os.path.dirname(os.path.abspath(__file__))
PwdPath = Pwd.split("/")
del PwdPath[-1]
modulePath = ""
for pp in PwdPath:
    modulePath += pp+"/"
Conf_path = modulePath+"conf"
sys.path.append(Conf_path)
## custom 모듈 
import AES_Cipher, LogModule, Passfile, sshModule
now2 = datetime.now()
toDay = now2.strftime('%Y%m%d')
lastweek = now2 - timedelta(days=7)
pastdate = lastweek.strftime('%Y%m%d')

##백업원본 위치
FW_confDir = "/home/sabangfeel/config_info/FW_config/temp_data"
L4_confDir = "/home/sabangfeel/config_info/L4_config/temp_data"
L3_confDir = "/home/sabangfeel/config_info/L3_config"

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    logger.error(Fore.RED+hostname+'서버 작업 중 에러가 발생하였습니다- FILE: {}, LINE: {} [{}], ERRMSG: {}'.format(filename, lineno, line.strip(), exc_obj)+Fore.RESET)

def Task():
    try:
        logger.info("방화벽 컨피그 백업파일 전송을 시작합니다.")
        os.chdir(FW_confDir)
        os.system("su - sabangfeel -c 'scp -rpP 5170 "+FW_confDir+"/"+toDay+"_Sabangnet_Office.conf sabangfeel@BACKUP03:/backup/FW_backup/FW_SYSCONFIG/Office/.'")
        os.system("su - sabangfeel -c 'scp -rpP 5170 "+FW_confDir+"/"+toDay+"_Sabangnet_FW1.conf sabangfeel@BACKUP03:/backup/FW_backup/FW_SYSCONFIG/IDC/.'")
         logger.info("백업파일 전송을 종료합니다.")
    except KeyboardInterrupt:
        logger.warn("프로그램을 강제종료 하였습니다.")
    except:
        PrintException()

def Task2():
    try:
        logger.info("L4컨피그 백업파일 전송을 시작합니다.")
        os.chdir(L4_confDir)
        os.system("su - sabangfeel -c 'scp -rpP 5170 "+L4_confDir+"/"+toDay+"_L4_Active_ns.conf sabangfeel@BACKUP03:/backup/L4_backup/config/.'")
        logger.info("백업파일 전송을 종료합니다.")
    except KeyboardInterrupt:
        logger.warn("프로그램을 강제종료 하였습니다.")
    except:
        PrintException()
def Task3():
    try:
        logger.info("스위치 컨피그 백업파일 전송을 시작합니다.")
        os.chdir(L3_confDir)
        os.system("su - sabangfeel -c 'scp -rpP 5170 "+L3_confDir+"/"+toDay+"_SB_HOST_SW1.conf sabangfeel@BACKUP03:/backup/SW_backup/.'")
        os.system("su - sabangfeel -c 'scp -rpP 5170 "+L3_confDir+"/"+toDay+"_SB_HOST_SW2.conf sabangfeel@BACKUP03:/backup/SW_backup/.'")
        os.system("su - sabangfeel -c 'scp -rpP 5170 "+L3_confDir+"/"+toDay+"_SB_HOST_SW3.conf sabangfeel@BACKUP03:/backup/SW_backup/.'")
        os.system("su - sabangfeel -c 'scp -rpP 5170 "+L3_confDir+"/"+toDay+"_SB_HOST_SW4.conf sabangfeel@BACKUP03:/backup/SW_backup/.'")
        os.system("su - sabangfeel -c 'scp -rpP 5170 "+L3_confDir+"/"+toDay+"_SB_HOST_SW5.conf sabangfeel@BACKUP03:/backup/SW_backup/.'")
        os.system("su - sabangfeel -c 'scp -rpP 5170 "+L3_confDir+"/"+toDay+"_SB_HOST_SW6.conf sabangfeel@BACKUP03:/backup/SW_backup/.'")
        os.system("su - sabangfeel -c 'scp -rpP 5170 "+L3_confDir+"/"+toDay+"_SB_HOST_SW7.conf sabangfeel@BACKUP03:/backup/SW_backup/.'")
        os.system("su - sabangfeel -c 'scp -rpP 5170 "+L3_confDir+"/"+toDay+"_SB_SVC_SW1.conf sabangfeel@BACKUP03:/backup/SW_backup/.'")
        os.system("su - sabangfeel -c 'scp -rpP 5170 "+L3_confDir+"/"+toDay+"_SB_SVC_SW2.conf sabangfeel@BACKUP03:/backup/SW_backup/.'")
             logger.info("백업파일 전송을 종료합니다.")
    except KeyboardInterrupt:
        logger.warn("프로그램을 강제종료 하였습니다.")
    except:
        PrintException()

if len(sys.argv) == 1:
    print("옵션을 아무것도 입력하지 않았습니다.\n-h 또는 --help 옵션을 이용하여 도움말 페이지를 읽어보시기 바랍니다.")
elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print("""
 FW,L4,SW 컨피그를 전송하는 스크립트입니다.
Usage: confBackup.py [OPTION]...
[OPTION]
   -h, --help		도움말 페이지를 확인할 수 있습니다.
   -F, --Fstart		방화벽 설정백업 파일 전송진행합니다.
   -L, --Lstart		L4장비 설정백업 파일 전송진행합니다.
   -W, --Wstart		SW장비 설정백업 파일 전송진행합니다.
    """)
elif sys.argv[1] == "-F" or sys.argv[1] == "-Fstart":
    logger = LogModule.Logging(Filename='confTrans', Day='7')
    try:
        AESC = AES_Cipher.AESCipher(key='mykey')
        Pw = Passfile.gubun("BACKUP03")
        BACKUP03Pw = AESC.decrypt(Pw)
        Task()
    except:
        PrintException()
elif sys.argv[1] == "-L" or sys.argv[1] == "--Lstart":
    logger = LogModule.Logging(Filename='confTrans', Day='7')
    try:
        AESC = AES_Cipher.AESCipher(key='mykey')
        Pw = Passfile.gubun("BACKUP03")
        BACKUP03Pw = AESC.decrypt(Pw)
        Task2()
    except:
        PrintException()
elif sys.argv[1] == "-W" or sys.argv[1] == "--Wstart":
    logger = LogModule.Logging(Filename='confTrans', Day='7')
    try:
        AESC = AES_Cipher.AESCipher(key='mykey')
        Pw = Passfile.gubun("BACKUP03")
        BACKUP03Pw = AESC.decrypt(Pw)
        Task3()
    except:
        PrintException()
else:
    print("잘못된 값을 입력하였습니다.\n-h 또는 --help 옵션을 이용하여 도움말 페이지를 읽어보시기 바랍니다.")
