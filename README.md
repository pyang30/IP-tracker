# IP-tracker
This script is used on Linux server which does not have a monitor.
Sometime, the server reboot or it's IP changed, but we can not know the new ip, 
so we cannot connect to it using SSH. 
This script can auto sends an email to the owner to report the new IP address.

USAGE:
1. Edit the script, 
  MAIL_LIST = ["youremail@xxx.com"]   //whem the email will be sent
  MAIL_HOST = "smtp.xxx.com"    // smtp server
  MAIL_USER = "sendsrc@xxx.com"  // who send the email, will show in the email.
  
  assume that the file is store at /usr/local/check_ip.py
  
2. In linux 
  # crontab -e 
  add " */5 * * * * python /usr/local/check_ip
  
Done！

  The system will check ip every 5 minites, if ip changed, it will send an email to MAIL_LIST users.
