pingCount=$1
pingLossTreshold=$2
pingDomain=$3

if [ $1 = "" ] || [ $2 = "" ] || [ $3 = "" ]
 then
 	echo "Usage netmon.sh pingCount pingLossTreshbold pingDomain"
 	exit 1
 fi

ping $pingDomain -c $pingCount > currentPing.txt

numberOfPacketLossString=`cat currentPing.txt | grep loss | awk '{ print $7 }'`
numberOfPacketLoss=`echo ${numberOfPacketLossString/%/}`

if [ $numberOfPacketLoss -lt $pingLossTreshold ]
 then
        rm currentPing.txt
 else
 	# Try to send email with included log files
        currentDate=`date +"%m-%d-%Y"`
        currentHour=`date +"%H-%M"`
        
        if [! -d "Logs" ]; then
  		mkdir Logs		
	fi
        
        # Move file to Logs folder
        mv currentPing.txt Logs/"PingLossAt_$currentDate_$curentHour.txt"
	
	# Generate email with attachments
	python2.7 ../mail/mail_message_poorInternet.py "$currentDate"	
fi

