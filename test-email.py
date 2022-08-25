import smtplib

gmail_user = "joshuamclymer@gmail.com"
gmail_password = "ur-never-gonna-get-my-passwords"

sent_from = gmail_user
to = ['jmc2437@columbia.edu']
subject = 'test subject'
body = 'test'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print('Email sent!')
except:
    print('Something went wrong...')