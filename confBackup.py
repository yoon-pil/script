#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys, os, datetime, linecache
from colorama import Fore
Pwd = os.path.dirname(os.path.abspath(__file__))
PwdPath = Pwd.split("/")
del PwdPath[-1]
modulePath = ""
for pp in PwdPath:
    modulePath += pp+"/"
Conf_path = modulePath+"conf"
sys.path.append(Conf_path)
##custom 모듈
import AES_Cipher, LogModule, Passfile, sshModule_ForFW
now = datetime.datetime.now()
toDay = now.strftime('%Y%m%d')

## 백업받을위치
FW_confDir = "/home/sabangfeel/config_info/FW_config/temp_data"
L4_confDir = "/home/sabangfeel/config_info/L4_config/temp_data"

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
        logger.info("백업 작업을 시작합니다.")
        os.chdir(FW_confDir)
        ssh = sshModule_ForFW.client('SabangOffice_FW', 'config_backup', FWpass)
        ssh.GET('sys_config', toDay+"_Sabangnet_Office.conf")
        ssh.scp.close()
        ssh.ssh.close()
        os.system("chown sabangfeel:sabangfeel "+FW_confDir+"/"+toDay+"_Sabangnet_Office.conf")
        logger.info("백업 작업을 종료합니다.")
    except KeyboardInterrupt:
        logger.warn("프로그램을 강제종료 하였습니다.")
    except:
        PrintException()

def Task2():
    try:
        logger.info("백업 작업을 시작합니다.")
        os.chdir(FW_confDir)
        ssh = sshModule_ForFW.client('SB-FW1', 'config_backup', FWpass)
        ssh.GET('sys_config', toDay+"_Sabangnet_FW1.conf")
        ssh.scp.close()
        ssh.ssh.close()
        os.system("chown sabangfeel:sabangfeel "+FW_confDir+"/"+toDay+"_Sabangnet_FW1.conf")
        logger.info("백업 작업을 종료합니다.")
    except KeyboardInterrupt:
        logger.warn("프로그램을 강제종료 하였습니다.")
    except:
        PrintException()

def Task3():
    try:
        logger.info("L4 Active장비백업 작업을 시작합니다.")
        os.chdir(L4_confDir)
        ssh = sshModule_ForFW.client('SB-L4-1', 'config_backup', L4pass)
        ssh.GET('/nsconfig/ns.conf', toDay+"_L4_Active_ns.conf")
        ssh.scp.close()
        ssh.ssh.close()
        os.system("chown sabangfeel:sabangfeel "+L4_confDir+"/"+toDay+"_L4_Active_ns.conf")
        #os.system("rm -rf "+FW_confDir+"/"+toDay+"_Sabangnet_Office.conf")
        logger.info("백업 작업을 종료합니다.")
    except KeyboardInterrupt:
        logger.warn("프로그램을 강제종료 하였습니다.")
    except:
        PrintException()

def Task4():
    try:
        logger.info("L4 Backup장비백업 작업을 시작합니다.")
        os.chdir(L4_confDir)
        ssh = sshModule_ForFW.client('SB-L4-2', 'config_backup', L4pass)
        ssh.GET('/nsconfig/ns.conf', toDay+"_L4_Backup_ns.conf")
        ssh.scp.close()
        ssh.ssh.close()
        os.system("chown sabangfeel:sabangfeel "+L4_confDir+"/"+toDay+"_L4_Backup_ns.conf")
        logger.info("백업 작업을 종료합니다.")
    except KeyboardInterrupt:
        logger.warn("프로그램을 강제종료 하였습니다.")
    except:
        PrintException()

if len(sys.argv) == 1:
    print("옵션을 아무것도 입력하지 않았습니다.\n-h 또는 --help 옵션을 이용하여 도움말 페이지를 읽어보시기 바랍니다.")
elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print("""
방화벽, L4  컨피그를 백업하는 스크립트입니다.
Usage: confBackup.py [OPTION]...
[OPTION]
   -h, --help		도움말 페이지를 확인할 수 있습니다.
   -Os, --Ostart	사방넷오피스방화벽 설정파일 백업을 진행합니다.
   -Is, --Istart	사방넷 IDC방화벽 설정파일 백업을 진행합니다.
   -As, --Astart	사방넷 L4장비(Active)  설정파일 백업을 진행합니다.
   -Bs, --Bstart	사방넷 L4장비(Backup) 설정파일 백업을 진행합니다.
    """)
elif sys.argv[1] == "-Os" or sys.argv[1] == "--Ostart":
    logger = LogModule.Logging(Filename='confBackup', Day='7')
    try:
        AESC = AES_Cipher.AESCipher(key='mykey')
        Pw = Passfile.gubun("SabangOffice_FW")
        FWpass = AESC.decrypt(Pw)
        Task()
    except:
        PrintException()

elif sys.argv[1] == "-Is" or sys.argv[1] == "--Istart":
    logger = LogModule.Logging(Filename='confBackup', Day='7')
    try:
        AESC = AES_Cipher.AESCipher(key='mykey')
        Pw = Passfile.gubun("SB-FW1")
        FWpass = AESC.decrypt(Pw)
        Task2()
    except:
        PrintException()
elif sys.argv[1] == "-As" or sys.argv[1] == "--Astart":
    logger = LogModule.Logging(Filename='confBackup', Day='7')
    try:
        AESC = AES_Cipher.AESCipher(key='mykey')
        Pw = Passfile.gubun("SB-L4-1")
        L4pass = AESC.decrypt(Pw)
        Task3()
    except:
        PrintException()

elif sys.argv[1] == "-Bs" or sys.argv[1] == "--Bstart":
    logger = LogModule.Logging(Filename='confBackup', Day='7')
    try:
        AESC = AES_Cipher.AESCipher(key='mykey')
        Pw = Passfile.gubun("SB-L4-2")
        L4pass = AESC.decrypt(Pw)
        Task4()
    except:
        PrintException()
else:
    print("잘못된 값을 입력하였습니다.\n-h 또는 --help 옵션을 이용하여 도움말 페이지를 읽어보시기 바랍니다.")
