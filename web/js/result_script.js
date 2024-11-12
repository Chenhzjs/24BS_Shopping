window.onload = function() {
    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = urlParams.get('search');

    const resultContainer = document.getElementById('resultContainer');

    if (searchQuery) {
        resultContainer.innerHTML = `<p>您搜索的内容是：<strong>${decodeURIComponent(searchQuery)}</strong></p>`;
    } else {
        resultContainer.innerHTML = '<p>未提供搜索内容。</p>';
    }
};