const ballotPrice = 10000;

function modifyPrice() {
    let total = 0;
    let ballotInputs = document.querySelectorAll('.balota-input');
    ballotInputs.forEach(input => {
        if (input.checked == true) {
            total += ballotPrice;
        }
    })

    let totalElement = document.querySelector('#total');
    totalElement.innerText = `$ ${total}`
}

// let ballotLabels = document.querySelectorAll('.balota-label');
// ballotLabels.forEach(label => {
//     label.addEventListener('click', modifyPrice);
// })

