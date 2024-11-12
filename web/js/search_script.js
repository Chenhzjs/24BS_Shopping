document.getElementById('searchForm').addEventListener('submit', function(e) {
    e.preventDefault(); // 阻止表单默认提交

    const query = document.getElementById('searchInput').value.trim();
    if (query) {
        // 跳转到 result.html 并传递查询参数
        window.location.href = `result.html?search=${encodeURIComponent(query)}`;
    } else {
        alert('请输入搜索内容');
    }
});