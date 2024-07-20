from email.mime.text import MIMEText
import smtplib
import conf

def send_mail(recipient,message) -> int:
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(conf.main_mail,conf.main_password)
            ms = MIMEText(message)
            ms['Subject'] = 'Отчет о премии'
            smtp.sendmail(conf.main_mail,recipient,ms.as_string())
            smtp.quit()
    except Exception as e:
        print(e)
        #need print
        return 1
    return 0
