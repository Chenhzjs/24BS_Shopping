document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // 获取用户输入
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    // const rememberMe = document.getElementById('rememberMe').checked;

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
    .then(response => {
        if (response.ok) {
            return response.text(); // 假设后端返回HTML内容
        } else {
            throw new Error('搜索请求失败');
        }
    })
    .then(html => {
        // console.log(html);
        // localStorage.removeItem('searchStyle');
        localStorage.removeItem('searchBody');
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const styleContent = Array.from(doc.querySelectorAll('style')).map(style => style.innerHTML).join('\n');
        const bodyContent = doc.body.innerHTML;

        // localStorage.setItem('searchStyle', styleContent);
        localStorage.setItem('searchBody', bodyContent);
        window.location.href = 'search.html';
    })
    .catch(error => {
        console.error('登录请求失败:', error);
        alert('发生错误，请稍后再试');
    });
});