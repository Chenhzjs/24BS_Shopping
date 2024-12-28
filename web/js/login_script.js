document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    // const rememberMe = document.getElementById('rememberMe').checked;

    if (username === '' || password === '') {
        alert('用户名或邮箱和密码不能为空');
        return;
    }
    // alert(`登录中... 用户名: ${username}, 记住我: ${rememberMe}`);
    const sendData = {
        username: username,
        password: password
    };


    fetch('http://localhost:5001/user/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(sendData) 
    })
    .then(response => {
        if (response.ok) {
            return response.text(); 
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