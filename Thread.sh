#!/bin/sh

logdir="/app/jeus8/logs/dump"
index="1 2 3"

echo "dump Start `date`" >> "$logdir/Tdump.log"
echo -e "컨테이너 명 입력하세요\ncontainer1 or container2"
## 사용자에게 입력받기
read Con_Name
echo "pid check start"
##pid 추출
pro_pid=`ps -ef | grep -v "grep" | grep "$Con_Name" | awk '{print $2}'`

echo "---------------------"
## 3번실행
for var in $index
do
   `jstack -l "$pro_pid" >> "$logdir"/Tdump_"$HOSTNAME"_"$Con_Name"_"$var".dmp`
   echo "execute $var `date`" >> "$logdir/Tdump.log"
   sleep 3s
done
echo "Execute done"
