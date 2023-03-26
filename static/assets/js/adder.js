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



















const billGenerator = document.querySelector('#bill-generator');
const codeValidator = document.querySelector('#code-validator');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const formSubmitter = document.querySelector('#form-submitter');


// PRODUCTION

// const codeValidationURL = 'https://web-production-aea2.up.railway.app/code_validation/';

// const linkCreationURL = 'https://web-production-aea2.up.railway.app/bill/';


// LOCALHOST

const codeValidationURL = 'http://127.0.0.1:8000/code_validation/';

const linkCreationURL = 'http://127.0.0.1:8000/bill/';




function getNumberOutOfString(string) {
    var numb = string.match(/\d/g);
    numb = numb.join("");
    return numb;

}


function validateCode() {
    let messageDiv = document.querySelector('#discount-code-message');
    let discountCode = document.querySelector('#discount_code').value;
    let billSubtotal = parseInt(getNumberOutOfString(document.querySelector('#bill-subtotal').innerText));
    if (discountCode) {
        const validationRequest = fetch(
            codeValidationURL,  
            {
                method: 'POST', 
                headers: {
                    'Content-Type': 'application.json', 
                    'X-CSRFToken': csrftoken
                }, 
                mode: 'same-origin',  
                body: JSON.stringify({
                    'discount_code': discountCode, 
                    'bId': bId
                })
            }
        )
        
        validationRequest.then(response => response.json())
        .then(data =>{
            // console.log('after validation request');
            // console.log(data);
            if (data.percentage) {
                messageDiv.setAttribute('class', 'correct-field');
                messageDiv.innerText = `El código es valido`;
                let discountValue = billSubtotal * (data.percentage/100);
                let billTotal = billSubtotal - discountValue;
                document.querySelector('#discount-values').innerText = `${data.percentage}% - $ ${discountValue}`;
                document.querySelector('#bill-total').innerText = billTotal; 
            } else if (data.error) {
                // console.log(data);
                messageDiv.setAttribute('class', 'incorrect-message');
                messageDiv.innerText = `${data.error}`;
            }
        }
        )
    } 
}


codeValidator.addEventListener('click', validateCode, false);



function addMissingFields() {

    var hiddenInputs = document.querySelectorAll('.hidden');
    if (hiddenInputs) {
        hiddenInputs.forEach(hiddenInput => {
            hiddenInput.remove();
        })
    }

    const dC = document.querySelector('#discount_code').value;
    var element1 = document.createElement('input');
    element1.setAttribute('type', 'hidden');
    element1.setAttribute('class', 'hidden');
    element1.name = 'ballot_ids';
    element1.value = bId;
    
    var element2 = document.createElement('input');
    element2.setAttribute('type', 'hidden');
    element2.setAttribute('class', 'hidden');
    element2.name = 'discount_code';
    element2.value = dC;
    
    var form = document.querySelector('#personal-data-form');
    form.append(element1);
    form.append(element2);
    
}


formSubmitter.addEventListener('click', addMissingFields);
