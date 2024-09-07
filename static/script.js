function monitorTraffic() {
    fetch('/traffic')
        .then(response => response.json())
        .then(data => {
            document.getElementById('traffic-results').textContent = JSON.stringify(data, null, 2);
        });
}

document.getElementById('node-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    fetch('/node-security', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('node-results').textContent = JSON.stringify(data, null, 2);
    });
});

document.getElementById('contract-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    fetch('/contract-audit', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('contract-results').textContent = JSON.stringify(data, null, 2);
    });
});

document.getElementById('vulnerability-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    fetch('/vulnerability-scan', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('vulnerability-results').textContent = JSON.stringify(data, null, 2);
    });
});
