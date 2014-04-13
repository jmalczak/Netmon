ping www.google.com -c 2 > currentPing.txt
packetLoss=`cat currentPing.txt | grep loss | awk -f netmon.awk`
packetLossNumber=`echo ${packetLoss/%/}`

if [ $packetLossNumber -gt 3 ]
 then
        rm currentPing.txt
 else
        currentDate=`date +"%m-%d-%Y_%H-%M"`
        mv currentPing.txt "bad_$currentDate.txt"
	python2.7 ../mail/mail_message_poorInternet.py "$currentDate"	
fi

