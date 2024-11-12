document.addEventListener('DOMContentLoaded', function() {
    const sendEmailBtn = document.querySelector('.send-to-email');
    const resetBtn = document.querySelector('.reset');
    const emailInput = document.getElementById('email');
    const codeSection = document.getElementById('code-section');
    const codeInput = document.getElementById('code');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');

    // 处理发送重置链接
    sendEmailBtn.addEventListener('click', function() {
        const email = emailInput.value.trim();

        // 验证邮箱格式
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        if (!emailPattern.test(email)) {
            alert('请输入有效的邮箱地址');
            return;
        }

        alert(`密码重置链接已发送至: ${email}`);
        
        // 模拟调用后台接口发送重置邮件
        const sendData = { step: '0', email: email };
        fetch('http://localhost:5001/user/forgotPassword', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(sendData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('密码重置邮件已发送');
                // 显示恢复码输入部分
                codeSection.style.display = 'block';
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('密码重置请求失败:', error);
            alert('发送失败，请稍后再试');
        });
    });

    // 处理恢复码验证
    resetBtn.addEventListener('click', function() {
        const code = codeInput.value.trim();
        if (!code) {
            alert('请输入恢复码');
            return;
        }

        // 模拟调用后台接口验证恢复码
        if (passwordInput.value !== confirmPasswordInput.value) {
            alert('密码和确认密码不一致');
            return;
        }
        const sendData = { step: '1', code: code,
                           password: passwordInput.value.trim()
         };
        fetch('http://localhost:5001/user/forgotPassword', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(sendData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('密码已成功重置');
                window.location.href = 'login.html';
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('恢复码验证失败:', error);
            alert('发生错误，请稍后再试');
        });
    });
});