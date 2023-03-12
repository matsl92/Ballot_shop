const csrftoken1 = document.querySelector('[name=csrfmiddlewaretoken]').value;

const request = fetch(
    'http://127.0.0.1:8000/test/', 
    {
        method: 'POST', 
        headers: {
            'Content-Type': 'application.json', 
            'X-CSRFToken': csrftoken1
        }, 
        mode: 'same-origin',  
        body: JSON.stringify({
            number_1: 3, 
            number_2: 4, 
            nickname: 'teo'
        })
    }
)