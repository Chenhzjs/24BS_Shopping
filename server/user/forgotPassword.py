from flask import request, jsonify
from werkzeug.security import check_password_hash
from . import user
from db import connection
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
def send_email_to(email, revocer_code):
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    username = 'chenhzjs@35p.org'
    password = 'Hz040719'  # 替换为你的邮箱密码或应用专用密码

    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = email
    msg['Subject'] = 'BuyCompare 密码恢复'

    # 添加邮件正文
    body = f'这是来自 BuyCompare 的密码恢复邮件。\n\n你的恢复码是{revocer_code}。'
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 启用 TLS 加密
        server.login(username, password)
        server.sendmail(username, email, msg.as_string())
        server.quit()
        print("邮件发送成功！")
    except Exception as e:
        print(f"邮件发送失败: {e}")


# 登录接口
@user.route('/forgotPassword', methods=['POST'])
def forgotPassword():
    data = request.get_json()  # 获取前端发送的 JSON 数据
    step = data.get('step')
    if (step == '0'):
        email = data.get('email')  # 用户名或邮箱
        conn = connection.get_db_connection("user")
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

        user = cursor.fetchone()  # 获取查询到的第一个用户记录

        cursor.close()
        conn.close()

        # 验证密码
        if user:  # 使用哈希密码进行验证
            # 发送邮件
            revocer_code = random.randint(100000, 999999)
            # insert recover code to db
            conn = connection.get_db_connection("user")
            cursor = conn.cursor(dictionary=True)
            cursor.execute("UPDATE users SET recover_code = %s WHERE email = %s", (revocer_code, email))
            conn.commit()
            cursor.close()
            conn.close()
            send_email_to(email, revocer_code)
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': '找不到当前邮箱'}), 401

    else:
        code = data.get('code')
        password = data.get('password')
        conn = connection.get_db_connection("user")
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE recover_code = %s", (code,))
        user = cursor.fetchone()
        if user:
            cursor.execute("UPDATE users SET password = %s WHERE recover_code = %s", (password, code))
            cursor.execute("UPDATE users SET recover_code = %s WHERE recover_code = %s", ('', code))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True})
        else :
            return jsonify({'success': False, 'message': '恢复码错误'}), 401



   