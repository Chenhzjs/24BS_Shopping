document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // 获取用户输入
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const rememberMe = document.getElementById('rememberMe').checked;

    // 检查用户名和密码是否为空
    if (username === '' || password === '') {
        alert('用户名或邮箱和密码不能为空');
        return;
    }
    // alert(`登录中... 用户名: ${username}, 记住我: ${rememberMe}`);
    // 构造要发送的请求数据
    const sendData = {
        username: username,
        password: password
    };

    // 使用 Fetch API 发送登录请求到后端
    fetch('http://localhost:5001/user/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(sendData) // 将登录数据转为 JSON 发送
    })
    .then(response => response.json()) // 解析 JSON 响应
    .then(data => {
        if (data.success) {
            // 登录成功，跳转到 main.html
            window.location.href = 'main.html';
        } else {
            // 登录失败，显示错误信息
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('登录请求失败:', error);
        alert('发生错误，请稍后再试');
    });
});