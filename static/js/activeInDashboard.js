// Active Button Ranking
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

// Active Pagination table
buttonsPagination.forEach(button => {
    button.addEventListener('click', () => {
        buttonsTren.forEach(btn => {
            btn.classList.remove('activePagination');
        });
        button.classList.add('activePagination');
    });
});

// Multi Select
function dropdown() {
    return {
        options: [],
        selected: [],
        show: false,
        open() {
            this.show = true
        },
        close() {
            this.show = false
        },
        isOpen() {
            return this.show === true
        },
        select(index, event) {

            if (!this.options[index].selected) {

                this.options[index].selected = true;
                this.options[index].element = event.target;
                this.selected.push(index);

            } else {
                this.selected.splice(this.selected.lastIndexOf(index), 1);
                this.options[index].selected = false
            }
        },
        remove(index, option) {
            this.options[option].selected = false;
            this.selected.splice(index, 1);


        },
        loadOptions() {
            const options = document.getElementById('select').options;
            for (let i = 0; i < options.length; i++) {
                this.options.push({
                    value: options[i].value,
                    text: options[i].innerText,
                    selected: options[i].getAttribute('selected') != null ? options[i].getAttribute('selected') : false
                });
            }


        },
        selectedValues() {
            return this.selected.map((option) => {
                return this.options[option].value;
            })
        }
    }
}