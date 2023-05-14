const activePage = window.location.pathname;
const navLinks = document.querySelectorAll('.itemActive').forEach(link => {
    if (link.href.includes(`${activePage}`)) {
        link.classList.add('active');
    }
})