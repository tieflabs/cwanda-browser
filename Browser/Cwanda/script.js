document.getElementById('searchForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var query = document.getElementById('searchQuery').value;
    var url = 'https://www.google.com/search?q=' + encodeURIComponent(query);
    var url = 'https://www.google.com/search?q=' + encodeURIComponent(query);
    window.location.href = url;
});
