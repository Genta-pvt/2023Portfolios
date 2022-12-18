import smtplib


class SendMail:
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.login('yuuki9665@gmail.com', 'gkndhxpiwvgsmemk')

    smtpobj.sendmail('yuuki9665@gmail.com', 'yuuki9665@gmail.com', 'subject')
    smtpobj.close()
