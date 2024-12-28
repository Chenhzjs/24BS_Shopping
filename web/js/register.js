document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!emailPattern.test(email)) {
        alert('请输入有效的邮箱地址');
        return;
    }

    if (password !== confirmPassword) {
        alert('密码和确认密码不一致');
        return;
    }
    // send the data to the backend

    const sendData = {
        username: username,
        email: email,
        password: password
    };

    fetch('http://localhost:5001/user/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(sendData),
    }) 
    .then(response => response.json()) 
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