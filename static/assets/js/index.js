const data = JSON.parse(
    document.getElementById('js-variables').textContent
);

// ------ Messages -------

const toastTrigger = data.msg[0];
const toastLiveExample = document.getElementById('notification');
const toast = new bootstrap.Toast(toastLiveExample,{
    delay: 10000
});

if (toastTrigger == 'suc') {
  toastLiveExample.classList.remove("bg-danger");
  toastLiveExample.classList.remove("bg-warning");
  toastLiveExample.classList.remove("bg-success");
  toastLiveExample.classList.add("bg-success");
  
  toastLiveExample.innerHTML = `
    <div class="toast-header">
      <i class="bi bi-check"></i>
      <strong class="me-auto"> ¡Felicidades!</strong>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body text-white">
      ${data.msg[1]}
    </div>
  `;

  toast.show();

} else if (toastTrigger == 'err' &&  data.link ) {
  toastLiveExample.classList.remove("bg-danger");
  toastLiveExample.classList.remove("bg-warning");
  toastLiveExample.classList.remove("bg-success");
  toastLiveExample.classList.add("bg-danger");
  
  toastLiveExample.innerHTML = `
    <div class="toast-header">
      <i class="bi bi-x"></i>
      <strong class="me-auto"> Lo sentimos</strong>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body text-white">
      ${data.msg[1]}<a href="${data.link}" style="color: #fff;"><strong>aquí</strong></a>
    </div>
  `;

  toast.show();

} else if (toastTrigger == 'err') {
    toastLiveExample.classList.remove("bg-danger");
    toastLiveExample.classList.remove("bg-warning");
    toastLiveExample.classList.remove("bg-success");
    toastLiveExample.classList.add("bg-danger");
    
    toastLiveExample.innerHTML = `
      <div class="toast-header">
        <i class="bi bi-x"></i>
        <strong class="me-auto"> Lo sentimos</strong>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      <div class="toast-body text-white">
        ${data.msg[1]}
      </div>
    `;
  
    toast.show();

}  else if (toastTrigger == 'war') {
    toastLiveExample.classList.remove("bg-danger");
    toastLiveExample.classList.remove("bg-warning");
    toastLiveExample.classList.remove("bg-success");
    toastLiveExample.classList.add("bg-warning");
    
    toastLiveExample.innerHTML = `
      <div class="toast-header">
        <i class="bi bi-exclamation-triangle-fill"></i>
        <strong class="me-auto">  Alerta</strong>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      <div class="toast-body text-white">
        ${data.msg[1]}
      </div>
    `;
  
    toast.show();
  }



// ------ Functionality -------

// The following code fetches and appends ballots returned from the backend
// when the page loads and when the search input gets modified.

const searchInput = document.getElementById('search-input');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const lotteryId = data.lottery_id;
const ballotFetchURL = data.ballot_fetch_url;
let nBallots;

if (window.innerWidth > 600) {
    nBallots = 27;
} else {
    nBallots = 12;
}

const ballots = [];

function modifyPriceAndSwitchCheckedState(inputId) {
    ballots.forEach(ballot => {
        if (ballot.id == inputId) {
            ballot.checked = !ballot.checked;
        }
    })

    let total = document.getElementById('total');
    let price = ballots.filter(ballot => ballot.checked).length * data.ballot_price;
    total.innerText = price;
}

function appendBallots(ballots) {
    var items, ballotWrapper, iconDiv, input, label, I;
    items = document.getElementById('items');
    
    for (let i = 0; i < ballots.length; i++) {

        // Create ballot wrapper with general elements and classes

        ballotWrapper = document.createElement('div');
        ballotWrapper.classList.add('ballot-wrapper', 'col-auto', 'icon-box');
        ballotWrapper.setAttribute("data-aos", "fade-up"); 

        iconDiv = document.createElement('div');
        iconDiv.classList.add('icon');

        input = document.createElement('input');
        input.classList.add('balota-input');
        input.setAttribute("type", "checkbox");
        input.setAttribute("name", "id");
        input.setAttribute("onclick", `modifyPriceAndSwitchCheckedState(${ballots[i].id})`);  // set value and id attributes with a for loop

        label = document.createElement('label');
        label.classList.add("balota-label", "icon") 

        I = document.createElement('i');
        I.classList.add('bi'); 

        // Add attributes whose values vary

        I.innerText = String(ballots[i].number);

        label.setAttribute("for", String(ballots[i].id));

        input.setAttribute("value", String(ballots[i].id));
        input.setAttribute("id", String(ballots[i].id));
        if (ballots[i].checked) {
            input.checked = true;
        }

        ballotWrapper.setAttribute("data-aos-delay", String(i*50));

        // Append elements

        label.append(I);

        iconDiv.append(input, label);

        ballotWrapper.append(iconDiv);

        items.append(ballotWrapper);

    }
    

}

function getBallotsFromBackend() {
    var request = fetch(ballotFetchURL, {
        method: 'POST', 
        headers:  {
            'Content-type':'application/json', 
            'X-CSRFToken': csrftoken
        }, 
        body: JSON.stringify({
            'lottery_id': lotteryId, 
            'name': 'mateo'
        })
    })
    request.then(response => response.json())
    .then(data => {
        for (let i = 0; i < data.length; i++) {
            ballots.push(data[i]);
        }

        appendBallots(ballots.slice(0, nBallots));

        
    })
}

window.addEventListener('load', getBallotsFromBackend);

function submitForm() {
    removeBallotWrappers();
    appendBallots(ballots.filter(ballot => ballot.checked == true));
    document.getElementById('ballot-form').submit();
}

function filterBallots(string, ballots) {
    var matchingBallots = ballots.filter(ballot => String(ballot.number).includes(string));
    return matchingBallots;
}

function removeBallotWrappers() {
    let ballotWrappers = document.querySelectorAll('.ballot-wrapper');
    ballotWrappers.forEach(wrapper => {
        wrapper.remove();
    })
}

function filterAndAppendBallots() {
    removeBallotWrappers();
    let filter = document.getElementById('search-input').value;
    let filteredBallots = filterBallots(String(filter), ballots);

    appendBallots(filteredBallots.slice(0, nBallots));
}

searchInput.addEventListener('keyup', filterAndAppendBallots);

window.addEventListener('load', appendBallots(ballots.slice(0, nBallots)));


