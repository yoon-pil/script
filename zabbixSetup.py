#!/usr/local/bin/python3
import sys, os, socket, linecache
from colorama import Fore
hostname = socket.gethostname()
Pwd = os.path.dirname(os.path.abspath(__file__))
PwdPath = Pwd.split("/")
del PwdPath[-1]
modulePath = ""
for pp in PwdPath:
    modulePath += pp+"/"
File_path = Pwd


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print(Fore.RED+'서버 확인 중 에러가 발생하였습니다- FILE: {}, LINE: {} [{}], ERRMSG: {}'.format(filename, lineno, line.strip(), exc_obj)+Fore.RESET)


try:
    print("Zabbix agent 설치")
    os.chdir(File_path)
    os.system("tar zxf zabbix-6.0.7.tar.gz")
    os.chdir(File_path+"/zabbix-6.0.7")
    os.system("./configure --prefix=/usr/local/zabbix --enable-agent")
    os.system("make && make install")
    os.system("groupadd zabbix")
    os.system("useradd -g zabbix zabbix -s /bin/false")
    with open('/usr/local/zabbix/etc/zabbix_agentd.conf', 'r+') as f:
        lines = []
        new_line1 = 'Server=172.17.1.149\n'
        new_line2 = 'ServerActive=172.17.1.149\n'
        new_line3 = 'Hostname='+hostname+'\n'
        new_line4 = '# Include=/usr/local/etc/zabbix_agentd.conf.d/*.conf\nInclude=/usr/local/zabbix/etc/zabbix_agentd.conf.d/*.conf\n'
        for line in f:
            if line.startswith('Server=127.0.0.1'):
                lines = lines + [new_line1]
            elif line.startswith('ServerActive=127.0.0.1'):
                lines = lines + [new_line2]
            elif line.startswith('Hostname=Zabbix server'):
                lines = lines + [new_line3]
            elif line.startswith('# Include=/usr/local/etc/zabbix_agentd.conf.d/*.conf'):
               lines = lines + [new_line4]
            else:
                lines = lines + [line]
        f.seek(0)
        f.writelines(lines)
        f.truncate()
    os.system("cp "+File_path+"/userparameter_*.conf /usr/local/zabbix/etc/zabbix_agentd.conf.d/")
    os.system("cp "+File_path+"/zabbix-6.0.7/misc/init.d/fedora/core/zabbix_agentd /etc/init.d/zabbix_agentd")
    os.system("sed -i 's/\/usr\/local/\/usr\/local\/zabbix/' /etc/init.d/zabbix_agentd")
    os.system("firewall-cmd --permanent --zone=public --add-port=10050/tcp")
    os.system("firewall-cmd --reload")

except KeyboardInterrupt:
    print("프로그램을 강제종료 하였습니다.\n")

except:
    PrintException()
