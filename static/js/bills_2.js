function hideBill() {
    let bill = document.getElementById('bill');
    bill.style.display = 'none';
}

document.addEventListener("DOMContentLoaded", hideBill);



const billGenerator = document.querySelector('#bill-generator');
const codeValidator = document.querySelector('#code-validator');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// PRODUCTION

// const codeValidationURL = 'https://web-production-aea2.up.railway.app/code_validation/';

// const linkCreationURL = 'https://web-production-aea2.up.railway.app/bill/';


// LOCALHOST

const codeValidationURL = 'http://127.0.0.1:8000/code_validation/';

const linkCreationURL = 'http://127.0.0.1:8000/bill/';



function addErrors(errors) {
    for (let error of errors) {
        let errorDiv = document.querySelector(`#${error[0]}-error`);
        errorDiv.innerText = error[1];
    }
}

function removeErrors() {
    for (element of document.getElementsByClassName('form-error')) {
        element.innerText = '';
    }
}


function validateCode() {
    let messageDiv = document.querySelector('#discount-code-message');

    let discountCode = document.querySelector('#discount_code').value;
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
            console.log('after validation request');
            console.log(data);
            if (data.percentage) {
                messageDiv.setAttribute('class', 'correct-field');
                messageDiv.innerText = `El código es valido, tienes un descuento del ${data.percentage}%.`;
            } else if (data.error) {
                console.log(data);
                messageDiv.setAttribute('class', 'incorrect-message');
                messageDiv.innerText = `${data.error}`;
            }
        }
        )
    } else {
        console.log('no discount code');
        messageDiv.innerText = "Este campo no es requerido."
    }
}

codeValidator.addEventListener('click', validateCode, false);

function ajaxRequest() {
    removeErrors();
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let firstName = document.querySelector('#first-name').value;
    let lastName = document.querySelector('#last-name').value;
    let email = document.querySelector('#email').value;
    let phoneNumber = document.querySelector('#phone-number').value;
    let discountCode = document.querySelector('#discount_code').value;
    // let ballot_ids = document.querySelectorAll('.ballot_ids');
    // let ballot_id_list = []
    // ballot_ids.forEach(element => ballot_id_list.push(element.defaultValue))
    const billRequest = fetch(
        linkCreationURL,  
        {
            method: 'POST', 
            headers: {
                'Content-Type': 'application.json', 
                'X-CSRFToken': csrftoken
            }, 
            mode: 'same-origin',  
            body: JSON.stringify({
                'first_name': firstName, 
                'last_name': lastName, 
                'email': email, 
                'phone_number': phoneNumber, 
                'ballot_ids': bId, 
                'discount_code': discountCode
            })
        }
    )

    billRequest.then(response => response.json())
    .then(data => {
        if (data.errors) {
            console.log('There are some errors');
            console.log(data);
            addErrors(data.errors);

        } else {
            document.querySelector('#bill-generator').remove();
            console.log('There are no errors');
            console.log(data);
            document.getElementById('page-1').remove();
            document.getElementById('client-name').innerText = data.client.name;
            document.getElementById('client-lastname').innerText = data.client.lastname;
            document.getElementById('client-email').innerText = data.client.email;
            document.getElementById('client-phone-number').innerText = data.client.phone_number;
            document.getElementById('value-1').innerText = data.value_1;
            document.getElementById('value-2').innerText = data.value_2;
            document.getElementById('epayco-button').href = data.link;

            let bill = document.getElementById('bill');
            bill.style.display = 'flex';
        }

        }
    )
}

billGenerator.addEventListener('click', ajaxRequest, false);

