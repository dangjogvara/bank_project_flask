document.body.addEventListener('click', function (e) {
    if (e.target.className === 'nav-link') {
        e.target.classList.add('active');
        console.log(e)
    }
});

