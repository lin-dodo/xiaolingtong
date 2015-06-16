# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

from_addr = "18814122757@139.com"
password = "XXXXXX"
#to_addr = "8674925@163.com"
smtp_server = "smtp.139.com"
def send_mail(text,to_addr = "8674925@163.com"):
	msg = MIMEText(text, 'plain', 'utf-8')
	msg['From'] = _format_addr(u'小灵通 <%s>' % from_addr)
	msg['To'] = _format_addr(u'小灵通用户 <%s>' % to_addr)
	msg['Subject'] = Header(u'来自小灵通的通知', 'utf-8').encode()

	server = smtplib.SMTP(smtp_server, 25)
	server.set_debuglevel(1)
	server.login(from_addr, password)
	server.sendmail(from_addr, [to_addr], msg.as_string())
	server.quit()
