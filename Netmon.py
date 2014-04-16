#!/opt/bin/python2.7

from SendGmail import SendGmail
import argparse
import sys
import re
import os
import datetime
from subprocess import Popen, PIPE

def Netmon():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', required=True, help='Gmail user')
	parser.add_argument('-p', required=True, help='Gmail password')
	parser.add_argument('-s', required=True, help='Sender address')
	parser.add_argument('-r', required=True, help='Recipient address')
	parser.add_argument('-d', help='Domain to ping', default='www.google.com')
	parser.add_argument('-c', help='Ping count', default=100)
	parser.add_argument('-t', help='Ping loss treshold', default=3)
	
	args = parser.parse_args()
	packetLoss = 0

	try:
		process = Popen('ping {0} -c {1}'.format(args.d, args.c), shell=True, stdout=PIPE)
		out, err = process.communicate()
		packetLoss = re.search('received, ([0-9]+)%', out).group(1)
	except:
		packetLoss = 100

	if int(packetLoss) > args.t :
		if not os.path.exists('Log'):
			os.makedirs('Log')

		currentDate = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
		fileName = 'Log/PingLoss_{0}.txt'.format(currentDate)
		f = open(fileName, 'w')
		f.write(out)
		f.close()

		try:
			mail = SendGmail(args.u, args.p)

			errorFiles = [ os.path.join('Log/',f) for f in os.listdir('Log/') if os.path.isfile(os.path.join('Log/',f)) ]
			errorFilesList = ', '.join(errorFiles)
			
			mailMessage = 'Ping loss {0}% has been observed at {1}.\nPlease take a look at ping output in attachment.\n\nBest regards Asus'.format(packetLoss, currentDate)
			mail.send(args.r, 'Home network ping loss {0}% at {1}'.format(packetLoss, currentDate), mailMessage, errorFilesList)
		finally:
			process = Popen('rm Log/*', shell=True)
			process.communicate()

if __name__ == "__main__":
	Netmon()