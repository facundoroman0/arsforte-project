function closeMessage(id) {
    const el = document.getElementById(id);
    if (el) {
        el.style.opacity = '0';
        el.style.transform = 'translateX(20px)';
        el.style.transition = 'all 0.3s ease';
        setTimeout(() => el.remove(), 300);
    }
}

document.querySelectorAll('.message').forEach(function (msg, index) {
    setTimeout(function () {
        closeMessage('message-' + (index + 1));
    }, 5000);
});