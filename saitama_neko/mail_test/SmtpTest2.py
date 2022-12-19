import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
 
from_address = 'zopopop0140@gmail.com'
to_address = 'zopopop0140@gmail.com'
bcc = ''
# 発行したアプリパスワード
app_password = 'odfivqnnquytcxlr'
subject = 'testタイトルです'
body = 'test内容です'
 
def create_message(from_addr, to_addr, bcc_addrs, subject, body):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
    print(type(msg))
    return msg
 
def send(from_addr, to_addrs, msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587, timeout=15)
    smtpobj.starttls()
    smtpobj.login(from_address, app_password)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()
 
message = create_message(from_address, to_address, bcc, subject, body)
send(from_address, to_address, message)
