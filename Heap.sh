#!/bin/sh
##로그파일 생성위치
logdir="/app/jeus8/logs/dump"


echo "dump Start `date`" >> "$logdir/Heapdump.log"
echo -e "컨테이너 명 입력하세요\ncontainer1 or container2"
read Con_Name
echo "pid check start"
pro_pid=`ps -ef | grep -v "grep" | grep "$Con_Name" | awk '{print $2}'`
echo "$Con_Name 's pid $pro_pid" >> "$logdir/Heapdump.log"

echo "---------------------"
echo "jmap 실행" 
`/etc/alternatives/jmap -dump:format=b,file="$logdir"/Heapdump_"$HOSTNAME"_"$Con_Name".dmp "$pro_pid"`
echo "execute `date`" >> "$logdir/Heapdump.log"

echo "Execute done"
