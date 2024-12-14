document.getElementById('searchForm').addEventListener('submit', function (e) {
    e.preventDefault(); // 阻止表单默认提交

    const query = document.getElementById('searchInput').value.trim();
    // 清除存储的 HTML
    localStorage.removeItem('savedSearchResult');
    if (query) {
        // 创建请求体
        fetch('http://localhost:5001/index/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }),
        })
        .then(response => {
            if (response.ok) {
                return response.text(); // 假设后端返回HTML内容
            } else {
                throw new Error('搜索请求失败');
            }
        })
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const styleContent = Array.from(doc.querySelectorAll('style')).map(style => style.innerHTML).join('\n');
            const bodyContent = doc.body.innerHTML;

            localStorage.setItem('searchResultStyle', styleContent);
            localStorage.setItem('searchResultBody', bodyContent);

            window.location.href = 'result.html';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('搜索失败，请稍后重试');
        });
    } else {
        alert('请输入搜索内容');
    }
});