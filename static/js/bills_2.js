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
                    'discount_code': discountCode
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
    document.querySelector('#bill-generator').remove();
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let _name = document.querySelector('#id_nombre').value;
    let lastname = document.querySelector('#id_apellido').value;
    let email = document.querySelector('#id_correo').value;
    let phone = document.querySelector('#id_celular').value;
    let discount_code = document.querySelector('#discount_code').value;
    let ballot_ids = document.querySelectorAll('.ballot_ids');
    let ballot_id_list = []
    ballot_ids.forEach(element => ballot_id_list.push(element.defaultValue))
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
                'nombre': _name, 
                'apellido': lastname, 
                'correo': email, 
                'celular': phone, 
                'ballot_ids': bId, 
                'discount_code': discount_code
            })
        }
    )

    billRequest.then(response => response.json())
    .then(data => {
        if (data.errors) {
            console.log('There are some errors');
            addErrors(data.errors);

        } else {
            console.log('There are no errors');
            console.log(data);
                
            // First time           __________________________
    
           
        }

        }
    )
}

billGenerator.addEventListener('click', ajaxRequest, false);

