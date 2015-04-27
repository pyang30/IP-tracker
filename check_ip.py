import os, smtplib, mimetypes, platform  
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage  
from email.mime.multipart import MIMEMultipart  
import socket
import fcntl
import struct
import time
 
MAIL_LIST = ["youremail@xxx.com"]  
MAIL_HOST = "smtp.xxx.com" 
MAIL_USER = "sendsrc@xxx.com"
#MAIL_FROM = MAIL_USER + "<" + MAIL_USER + ">" 
MAIL_FROM = platform.uname()[1]
OLD_IP_FILE = "/var/local/oldip"
RESET_INET_FILE = "cp /etc/network/orginterface /etc/network/interfaces"
RESTART_NETWORK_CMD = "/etc/init.d/networking restart"
GET_DHCP_CMD = "dhclient eth0"

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
		return socket.inet_ntoa(fcntl.ioctl(
			s.fileno(),
			0x8915,  # SIOCGIFADDR
			struct.pack('256s', ifname[:15])
		)[20:24])
    except Exception, errmsg:
		return ""

def get_old_ip():
	if not os.path.isfile(OLD_IP_FILE):
		os.system("touch " + OLD_IP_FILE)
		fd = open(OLD_IP_FILE, 'w')
		fd.write("")
		fd.close()
		return ""
	else:
		fd = open(OLD_IP_FILE, 'r')
		try:
			old_ip = fd.readline()
			fd.close()
			return old_ip
			
		except Exception, msg:
			fd.close()
			fd = open(OLD_IP_FILE, 'w')
			fd.write("")
			fd.close()
			return ""

def write_ip_back(new_ip):
	#print "func new ip = " + new_ip
	try:
		fd = open(OLD_IP_FILE, 'w')
		fd.write(new_ip)
		fd.close()
	except Exception, msg:
	#	print "exception"
		fd.close()	

def send_mail(subject, content, filename = None):  
    try:  
        message = MIMEMultipart()  
        message.attach(MIMEText(content))  
        message["Subject"] = subject  
        message["From"] = MAIL_FROM  
        message["To"] = ";".join(MAIL_LIST)  
        if filename != None and os.path.exists(filename):  
            ctype, encoding = mimetypes.guess_type(filename)  
            if ctype is None or encoding is not None:  
                ctype = "application/octet-stream" 
            maintype, subtype = ctype.split("/", 1)  
            attachment = MIMEImage((lambda f: (f.read(), f.close()))(open(filename, "rb"))[0], _subtype = subtype)  
            attachment.add_header("Content-Disposition", "attachment", filename = filename)  
            message.attach(attachment)  
 
        smtp = smtplib.SMTP(MAIL_HOST, 25)  
        smtp.sendmail(MAIL_USER, MAIL_LIST, message.as_string())  
        smtp.quit()  
 
        return True 
    except Exception, errmsg:  
        #print "Send mail failed to: %s" % errmsg  
        return False 

def send_ip(old_ip, new_ip):
	str = MAIL_FROM + "'ip has changed from " + old_ip + " to " + new_ip
	print str
	if send_mail(MAIL_FROM + "'ip Has Changed.", str, None):
		print "Done"
	else:
		print "Failed"
	 
if __name__ == "__main__":  
#	os.system("dhclient eth0")
	old_ip = get_old_ip()
	#print "old ip = " + old_ip
	new_ip = get_ip_address("eth0")
	#print "new ip = " + new_ip
	if new_ip == "":
	#	print "new ip is null"
		os.system(RESET_INET_FILE)
		os.system(RESTART_NETWORK_CMD)
		os.system(GET_DHCP_CMD)
		new_ip = get_ip_address("eth0")
		time.sleep(5)
		write_ip_back(new_ip)
		send_ip(old_ip, new_ip)
	else:
		if new_ip == old_ip:
			#print "new_ip == old_ip"
			pass
		else:
			#print "write back ip"	
			write_ip_back(new_ip)	
			send_ip(old_ip, new_ip)
