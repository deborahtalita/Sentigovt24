const buttonsRanking = document.querySelectorAll('.rankingButton');
const buttonsTren = document.querySelectorAll('.chooseChart');

buttonsRanking.forEach(button => {
    button.addEventListener('click', () => {
        buttonsRanking.forEach(btn => {
            btn.classList.remove('activeRanking');
        });
        button.classList.add('activeRanking');
    });
});

buttonsTren.forEach(button => {
    button.addEventListener('click', () => {
        buttonsTren.forEach(btn => {
            btn.classList.remove('activeTren');
        });
        button.classList.add('activeTren');
    });
});

buttonsPagination.forEach(button => {
    button.addEventListener('click', () => {
        buttonsTren.forEach(btn => {
            btn.classList.remove('activePagination');
        });
        button.classList.add('activePagination');
    });
});