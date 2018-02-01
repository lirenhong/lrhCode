#! coding: utf-8
import os
import commands
os.chdir('/sysvol/apphome/app/ShareMgnt/boost')
pid = commands.getstatusoutput("ps -ef |grep sharemgnt_server |grep -v grep|sed -n 2p|awk '{print $2}'")[1]
if not pid:
	print "Starting ShareMgnt services..."
	os.system('chmod +x sharemgnt')
	os.system('./sharemgnt start &> /dev/null')
	print "Start successful!"
else:
	print "Stopping ShareMgnt services..."
	os.system('chmod -x sharemgnt')
	os.environ['pid'] = pid
	os.system("kill -9 $pid")
	print "Stop successful!"
	

 
