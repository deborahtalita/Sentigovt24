// Active menu sidenav
const activePage = window.location.pathname;
const navLinks = document.querySelectorAll('.itemActive').forEach(link => {
    if (link.href.includes(`${activePage}`)) {
        link.classList.add('active');
    }
})

// Href
function goToDetailPage(url) {
    window.location.href = url;
}