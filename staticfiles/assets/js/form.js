// ----- Form functionality ----

const data = JSON.parse(
    document.getElementById('js-variables').textContent
);

const bP = data.ballot_price;
const codeValidationURL = data.code_validation_url;
const linkCreationURL = data.link_creation_url;
const codeValidator = document.querySelector('#code-validator');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const formSubmitter = document.querySelector('#form-submitter');
const bId = data.bId;

function getNumberOutOfString(string) {
    var numb = string.match(/\d/g);
    numb = numb.join("");
    return numb;

}

function validateCode() {
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
                document.querySelector('#bill-total').innerText = billSubtotal;
            }
        }
        )
    } 
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

codeValidator.addEventListener('click', validateCode, false);

formSubmitter.addEventListener('click', addMissingFields);

// Prevent Double Submits
document.querySelectorAll('#personal-data-form').forEach(form => {
	form.addEventListener('submit', (e) => {
		// Prevent if already submitting
		if (form.classList.contains('is-submitting')) {
			e.preventDefault();
		}
		
		// Add class to hook a visual indicator on
		form.classList.add('is-submitting');
	});
});
