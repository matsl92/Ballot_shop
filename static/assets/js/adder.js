const data2 = JSON.parse(
    document.getElementById('context-variables').textContent
);

console.log(data2);

const bP = data2.ballot_price;

function modifyPrice() {
    let total = 0;
    let ballotInputs = document.querySelectorAll('.balota-input');
    ballotInputs.forEach(input => {
        if (input.checked == true) {
            total += bP;
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

const codeValidationURL = 'https://web-production-31f8.up.railway.app/code_validation/';

const linkCreationURL = 'https://web-production-31f8.up.railway.app/bill/';


// LOCALHOST

// const codeValidationURL = 'http://127.0.0.1:8000/code_validation/';

// const linkCreationURL = 'http://127.0.0.1:8000/bill/';



// Prevent Double Submits
document.querySelectorAll('#personal-data-form').forEach(form => {
	form.addEventListener('submit', (e) => {
		// Prevent if already submitting
		if (form.classList.contains('is-submitting')) {
			e.preventDefault();
            console.log('Prevented default');
		}
		
		// Add class to hook our visual indicator on
		form.classList.add('is-submitting');
        console.log('added class is-submitting');
	});
});




function getNumberOutOfString(string) {
    var numb = string.match(/\d/g);
    numb = numb.join("");
    return numb;

}


const bId = data2;
function validateCode() {
    console.log(data2);
    console.log(bId);
    console.log('hey there');
    let messageDiv = document.querySelector('#discount-code-message');
    let discountCode = document.querySelector('#discount_code').value;
    let billSubtotal = parseInt(getNumberOutOfString(document.querySelector('#bill-subtotal').innerText));
    if (true) {
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
            if (data.percentage) {
                let discountValue = billSubtotal * (data.percentage/100);
                let billTotal = billSubtotal - discountValue;
                messageDiv.innerText = `${data.percentage}% = $ ${discountValue}`;
                document.querySelector('#bill-total').innerText = billTotal; 
            } else if (data.error) {
                messageDiv.setAttribute('class', 'incorrect-message');
                messageDiv.innerText = `${data.error}`;
                document.querySelector('#discount-values').innerText = '';
                document.querySelector('#bill-total').innerText = billSubtotal;
            }
        }
        )
    } 
}


if (codeValidator) {

    codeValidator.addEventListener('click', validateCode, false);
}



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


if (formSubmitter) {
    
    formSubmitter.addEventListener('click', addMissingFields);
}


