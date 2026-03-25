function addExpense() {
    let hardware_part = document.getElementById('hardware_part').value.trim();
    let price = document.getElementById('price').value;

    if (!hardware_part || !price) {
        alert('Пожалуйста, заполните все поля.');
        return;
    }

    fetch('/add', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            hardware_part: hardware_part,
            price: parseInt(price)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            location.reload();  // 刷新页面显示新数据
        } else {
            alert('Ошибка при добавлении');
        }
    })
    .catch(err => alert('Ошибка сети'));
}

function clearAll() {
    if (!confirm('Вы уверены, что хотите удалить все записи?')) return;
    fetch('/clear', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                location.reload();
            } else {
                alert('Ошибка при очистке');
            }
        })
        .catch(err => alert('Ошибка сети'));
}