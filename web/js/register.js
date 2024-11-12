document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // 简单的邮箱验证（更复杂的验证可以用正则表达式）
    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!emailPattern.test(email)) {
        alert('请输入有效的邮箱地址');
        return;
    }

    // 密码和确认密码是否一致
    if (password !== confirmPassword) {
        alert('密码和确认密码不一致');
        return;
    }
    // send the data to the backend

    const sendData = {
        username: username,
        password: password
    };

    // 发送 post
    fetch('http://localhost:5001/user/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(sendData),
    }) 
    .then(response => response.json()) // 解析 JSON 响应
    .then(data => {
        if (data.success) {
            window.location.href = 'login.html';
            localStorage.setItem('username', username);
            localStorage.setItem('password', password);
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('注册请求失败:', error);
        alert('发生错误，请稍后再试');
    });
});