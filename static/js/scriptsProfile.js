function changePassword() {
    document.getElementById("changePassword").classList.toggle("active");
    $('body').addClass('overflow-hidden');
}

function closeModal() {
    $('body').removeClass('overflow-hidden');
}