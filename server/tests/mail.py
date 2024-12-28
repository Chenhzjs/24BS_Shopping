import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

subject = "测试邮件"  
body = "hello, my name is chenhz."  

sender_email = "xxx@qq.com"  
receiver_email = "xxx@qq.com"  

password = "ehamgwpzehuseced"  

smtp_server = "smtp.qq.com"
smtp_port = 465

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

msg.attach(MIMEText(body, 'plain'))

try:
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:  
        server.login(sender_email, password)  
        server.sendmail(sender_email, receiver_email, msg.as_string())  
        server.quit()
        print("邮件发送成功！")
except Exception as e:
    print(f"邮件发送失败: {e}")
