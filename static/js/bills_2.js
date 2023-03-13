const billGenerator = document.querySelector('#bill-generator');
const codeValidator = document.querySelector('#code-validator');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


function validateCode() {
    let discountCode = document.querySelector('#discount_code').value;
    if (discountCode) {
        const validationRequest = fetch(
            // 'https://web-production-aea2.up.railway.app/code_validation/', 
            'http://127.0.0.1:8000/code_validation/', 
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
        }
        )
    } else {
        console.log('no discount code');
    }
}

codeValidator.addEventListener('click', validateCode, false);

function ajaxRequest() {
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
        // 'https://web-production-aea2.up.railway.app/bill/', 
        'http://127.0.0.1:8000/bill/', 
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
                'ballot_ids': ballotIdList, 
                'discount_code': discount_code
            })
        }
    )

    // .then((response) => {
    //     if (!response.ok) {
    //         console.log('There was an error');
    //         // console.log(response.json());
    //         // response.json().er
    //     } else {
    //         console.log('The request went well');
    //         console.log(response.json());
    //     }
    // }, (error) => {
    //     console.log(error);
    //     console.log(error.json());
    // })
    billRequest.then(response => response.json())
    .then(data => {

        if (data.errors) {
            console.log('There are some errors');
            console.log(data.errors)
        } else {
            console.log('There are no errors');
            console.log(data);
            if (document.querySelector('#ajax-div')) {
                document.querySelector('#ajax-div').remove();
            };
                
            // First time           __________________________
    
            // create bill
            let bill = document.createElement('div');
            bill.setAttribute('id', 'bill');
    
            // create ballots
            data.ballot_ids.forEach(function(id) {
                const div = document.createElement("div");
                const num = document.createElement("u");
                num.innerText = id;
                div.append(num);
                bill.append(div);
            });
    
            // create personal data
    
            // create value 1
            let value1 = document.createElement('div');
            let price1 = document.createElement('u');
            price1.innerText = data.value_1;
            value1.append(price1);
            bill.append(value1);
    
            // create value 2
            let value2 = document.createElement('div');
            let price2 = document.createElement('u');
            price2.innerText = data.value_2;
            value2.append(price2);
            bill.append(value2);
    
            // add values to bill
            
            // create ajax-div 
            let ajaxDiv = document.createElement('div');
            ajaxDiv.setAttribute('id', 'ajax-div');
    
            // add bill to ajaxDiv
            ajaxDiv.append(bill);
    
            // create hidden input value1
            let input1 = document.createElement('input');
            input1.type = 'hidden';
            input1.setAttribute('id', "value-1");
            input1.value = data.value_1
            input1.name = "value_1";
            ajaxDiv.append(input1);
            
            // create hidden input value2
            let input2 = document.createElement('input');
            input2.type = 'hidden';
            input2.setAttribute('id', "value-2");
            input2.value = data.value_2
            input2.name = "value_2";
            ajaxDiv.append(input2);
            
            // create hidden input clientId
            let clientId = document.createElement('input');
            clientId.type = 'hidden';
            clientId.setAttribute('id', "client-id");
            clientId.value = data.client.id
            clientId.name = "client_id";
            ajaxDiv.append(clientId);
    
            // create hidden input discountId
            let discountId = document.createElement('input');
            discountId.type = 'hidden';
            discountId.setAttribute('id', "discount-id");
            discountId.value = data.discount_id
            discountId.name = "discount_id";
            ajaxDiv.append(discountId);
            
            // create hidden input ballotId
            let ballotId = document.createElement('input');
            ballotId.type = 'hidden';
            ballotId.setAttribute('id', "ballot-id");
            ballotId.value = data.ballot_ids
            ballotId.name = "ballot_id";
            ajaxDiv.append(ballotId);
    
            // // create submit input
            // let input = document.createElement('input');
            // input.type = 'submit';
            // input.setAttribute('id', 'epayco-button');
            // input.value = 'ePayco';
            // ajaxDiv.append(input);

            // create link
            let link = document.createElement('a');
            link.setAttribute('href', data.link);
            link.setAttribute('id', 'epayco-link');
            // link.value = 'ePayco2';
            link.innerText = 'epayco2';
            ajaxDiv.append(link);
            
            // add values and bill to ajax-div
            
            
            // select bill-form
            form = document.querySelector('#bill-form');
            
            // add ajax-div to bill-form
            form.append(ajaxDiv);
        }

        }
    )
        

    // .then(data)
}





billGenerator.addEventListener('click', ajaxRequest, false);

// billGenerator.preventDefault();
    
    
//     request.then(response => response.text())
//     .then((data) => {
//         console.log(data);
//         data.ballot_id_list.forEach(
//             function(id) {
//                 div = document.createElement("div");
//                 num = document.createElement("u");
//                 num.innerText = id;
//                 div.append(num);
//                 document.body.append(div);
//             }
//         )
//     });
        
// };


// propNames.forEach((name) => {
//     const desc = Object.getOwnPropertyDescriptor(obj, name);
//     Object.defineProperty(copy, name, desc);
//   });