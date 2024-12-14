from flask import request, jsonify
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from . import user
from db import connection
import random
from index.mail import send_email_to

# 登录接口
@user.route('/forgotPassword', methods=['POST'])
def forgotPassword():
    data = request.get_json()  # 获取前端发送的 JSON 数据
    step = data.get('step')
    
    if step == '0':
        email = data.get('email')  # 用户名或邮箱
        conn = connection.get_db_connection("user")
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()  # 获取查询到的第一个用户记录

        cursor.close()
        conn.close()

        # 验证用户存在
        if user:
            # 生成验证码
            recover_code = random.randint(100000, 999999)
            # 当前时间
            timestamp = datetime.now()
            
            # 更新数据库中的验证码和时间戳
            conn = connection.get_db_connection("user")
            cursor = conn.cursor(dictionary=True)
            cursor.execute("UPDATE users SET recover_code = %s, revocer_time = %s WHERE email = %s", 
                           (recover_code, timestamp, email))
            conn.commit()
            cursor.close()
            conn.close()

            # 发送验证码邮件
            subject = f"您的验证码是：{recover_code}"  # 邮件主题
            body = f'尊敬的用户，\n\n您好！您的验证码是：{recover_code}。请在 10 分钟内输入验证码完成验证。\n\n如果您没有进行此操作，请忽略本邮件。\n\n感谢您的使用！\n\n[公司名称] 客服团队\n'  # 邮件正文内容
            
            send_email_to(email, subject, body, 1)
            return jsonify({'success': True})
        
        return jsonify({'success': False, 'message': '找不到当前邮箱'}), 401

    else:
        code = data.get('code')
        password = data.get('password')
        conn = connection.get_db_connection("user")
        print("step = 1")
        print(code, password)
        cursor = conn.cursor(dictionary=True)

        # 查询数据库中的验证码及其时间戳
        cursor.execute("SELECT * FROM users WHERE recover_code = %s", (code,))
        user = cursor.fetchone()

        if user:
            # 检查验证码是否过期（10分钟内有效）
            recover_code_timestamp = user['recover_time']
            expiration_time = recover_code_timestamp + timedelta(minutes=10)
            
            if datetime.now() > expiration_time:
                cursor.close()
                conn.close()
                return jsonify({'success': False, 'message': '验证码已过期'}), 401

            if len(password) < 6:
                return jsonify({'success': False, 'message': '密码长度不能小于 6 位'}), 400
            if not password.isalnum():
                return jsonify({'success': False, 'message': '密码只能包含数字和字母'}), 400
            
            # 验证码有效，更新密码
            cursor.execute("UPDATE users SET password = %s WHERE recover_code = %s", (generate_password_hash(password), code))
            cursor.execute("UPDATE users SET recover_code = '', recover_time = NULL WHERE recover_code = %s", (code,))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True})
        else:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '恢复码错误'}), 401