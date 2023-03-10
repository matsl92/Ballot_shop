

function ajaxRequest() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let _name = document.querySelector('#id_nombre').value;
    let lastname = document.querySelector('#id_apellido').value;
    let email = document.querySelector('#id_correo').value;
    let phone = document.querySelector('#id_celular').value;
    let discount_code = document.querySelector('#discount_code').value;
    let ballot_ids = document.querySelectorAll('.ballot_ids');
    let ballot_id_list = []
    ballot_ids.forEach(element => ballot_id_list.push(element.defaultValue))
    const request = fetch(
        'http://127.0.0.1:8000/test/', 
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
                'ballot_ids': ballot_id_list, 
                'discount_code': discount_code
            })
        }
    )

    
    request.then(response => response.json())
    .then(data => {

        let inputIds = ['value_1', 'value_2', 'client_id', 'discount_id', 'ballot_id'];

        if (document.querySelector('#ajax-div')) {
            document.querySelector('#ajax-div').remove();
        } else {
            
            // First time           __________________________

            // create bill ______________

            // create ballots

            // create personal data

            // create value 1

            // create value 2

            // add values to bill

            // create bill-form _________

            // create hidden input value1

            // create hidden input value2

            // create hidden input clientId

            // create hidden input discountId

            // create hidden input ballotId

            // add values to bill-form
            
            // create ajax-div 

            // append bill and bill-form to ajax-div

            // append ajax-div to document
            

            console.log('there was not a bill form');
            data.ballot_ids.forEach(function(id) {
                const div = document.createElement("div");
                const num = document.createElement("u");
                num.innerText = id;
                div.append(num);
                document.body.append(div);
            });

            // create prices

            if (data.value_1 != data.value_2) {
                let value1 = document.createElement('div');
                let price1 = document.createElement('u');
                price1.innerText = data.value_1;
                value1.append(price1);
                document.body.append(value1);
            };

            let value2 = document.createElement('div');
            let price2 = document.createElement('u');
            price2.innerText = data.value_2;
            value2.append(price2);
            document.body.append(value2);

            // create form

            let form = document.createElement('form');
            form.id = 'bill-form'
            form.action = '/checkout/';
            form.method = 'POST';
            form.csrftoken = csrftoken;


            // create and add values to form

            inputIds.forEach(function(id) {
                let input = document.createElement('input');
                input.type = 'hidden';
                input.setAttribute('id', id);
                input.value = 
                form.append(input)
            });




            // add form

            document.body.append(form);


        };

            
            
            // prices

            

            
            // hidden values

            // if (!document.querySelector('#bill-form')) {
            //     console.log('New!!!');
                
            //     
                
            //     let input1 = document.createElement('input');
            //     input1.type = 'hidden';
            //     input1.setAttribute("id", 'value_1');
            //     input1.name = 'value_1';
            //     input1.value = data.value_1;
            //     form.append(input1);
                
            //     let input2 = document.createElement('input');
            //     input2.type = 'hidden';
            //     input1.setAttribute("id", 'value_2');
            //     input2.name = 'value_2';
            //     input2.value = data.value_2;
            //     form.append(input2);
                
            //     let input3 = document.createElement('input');
            //     input3.type = 'hidden';
            //     input1.setAttribute("id", 'client_id');
            //     input3.name = 'client_id';
            //     input3.value = data.client_id;
            //     form.append(input3);
                
            //     let input4 = document.createElement('input');
            //     input4.type = 'hidden';
            //     input1.setAttribute("id", 'ballot_ids');
            //     input4.name = 'ballot_ids';
            //     input4.value = data.ballot_ids;
            //     form.append(input4);
                
            //     const input5 = document.createElement('input');
            //     input5.type = 'submit';
            //     input5.value = 'ePayco';
            //     form.append(input5);
                
            //     document.body.append(form);
            // } else {
            //     let input1 = document.getElementById('value_1');
            //     console.log(data.value_1);
            //     console.log(input1)
            //     console.log(input1.value);
            //     input1.value = data.value_1;
            //     let input2 = document.getElementById('value_2');
            //     input2.value = data.value_2;
            //     let input3 = document.getElementById('client_id');
            //     input3.value = data.client_id;
            //     let input4 = document.getElementById('ballot_ids');
            //     input4.value = data.ballot_ids;
            // };
        }
    )
        

    // .then(data)
}



const billGenerator = document.querySelector('#bill-generator');

billGenerator.addEventListener('click', ajaxRequest);
    
    
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