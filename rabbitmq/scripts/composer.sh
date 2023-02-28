#!/bin/bash

COUNT=0
# backend-server
HOST=10.0.0.108
ping -q -w 3 -i2 $HOST 2>&1 >/dev/null
OFFLINE=$?
if [ $OFFLINE -eq 1 ];
then
	echo "Back End Device is offline"
	echo "Checking Next Device"
	COUNT=$((COUNT+1))
else
	echo "Back End Device is online...Wait"
	sleep 2
	ssh -t it490admin@$HOST "sh /home/it490admin/Projects/Date-App/back-end/scripts/start-up.sh"
fi


# frontend-server
HOST1=10.0.0.156
ping -q -w 3 -i2 $HOST1 2>&1 >/dev/null
OFFLINE1=$?
if [ $OFFLINE1 -eq 1 ];
then
	echo "Front End Device is offline"
	echo "Checking Next Device"
	COUNT=$((COUNT+1))
else
	echo "Front End Device is online...Wait"
	sleep 2
	ssh -t it490admin@$HOST1 "sh /home/it490admin/Projects/Date-App/front-end/scripts/start-up.sh"
fi


# database-server
HOST2=10.0.0.207
ping -q -w 3 -i2 $HOST2 2>&1 >/dev/null
OFFLINE2=$?
if [ $OFFLINE2 -eq 1 ];
then
	echo "Database Device is offline"
	COUNT=$((COUNT+1))
else
	echo "Database Device is online...Wait"
	sleep 2
	ssh -t it490admin@$HOST2 "sh /home/it490admin/Projects/Date-App/mariadb/scripts/start-up.sh"
fi

if [ $COUNT -eq 1 ]; then
	echo "One device is offline"
elif [ $COUNT -eq 2 ]; then
	echo "Two devices are offline"
elif [ $COUNT -eq 3 ]; then
	echo "All other devices are offline"
elif [ $COUNT -eq 0 ]; then
	echo "All other devices are online"
fi
