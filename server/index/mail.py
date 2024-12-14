import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def send_email_to(email, subject, body, debug):
    
    if not debug:
        # 发件人和收件人邮箱
        sender_email = "2559488236@qq.com"  # 发件人邮箱
        receiver_email = email  # 收件人邮箱

        # QQ 邮箱授权码
        password = "ehamgwpzehuseced"  # 使用你QQ邮箱的授权码

        # SMTP服务器设置
        smtp_server = "smtp.qq.com"
        smtp_port = 465

        # 创建邮件消息
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # 邮件正文
        msg.attach(MIMEText(body, 'plain'))

        try:
            # 连接到SMTP服务器并发送邮件
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:  # 使用 SSL 加密
                server.login(sender_email, password)  # 登录邮箱
                server.sendmail(sender_email, receiver_email, msg.as_string())  # 发送邮件
                server.quit()
                print("邮件发送成功！")
        except Exception as e:
            print(f"邮件发送失败: {e}")
    else:
        print(f"收件人邮箱：{email}")
        print(f"邮件主题：{subject}")
        print(f"邮件内容：{body}")
   