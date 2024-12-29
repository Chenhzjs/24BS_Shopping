import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def send_email_to(email, subject, body, debug):
    
    if not debug:

        sender_email = "2559488236@qq.com"  
        receiver_email = email  


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
    else:
        print(f"收件人邮箱：{email}")
        print(f"邮件主题：{subject}")
        print(f"邮件内容：{body}")
   