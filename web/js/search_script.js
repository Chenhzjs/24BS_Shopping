document.getElementById('searchForm').addEventListener('submit', function (e) {
    e.preventDefault(); 

    const query = document.getElementById('searchInput').value.trim();
    localStorage.removeItem('savedSearchResult');
    if (query) {
        fetch('http://localhost:5001/index/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }),
        })
        .then(response => {
            if (response.ok) {
                return response.text(); 
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