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



// ------ Ballot functionality -------

// The following code defines some basic functions and then some complex ones
// which include one or more basic functions.

const searchInput = document.getElementById('search-input');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const lotteryId = data.lottery_id;
const ballotFetchURL = data.ballot_fetch_url;
const randomBallotSelector = document.getElementById('random-ballot-selector');
const ballots = [];
let selectedBallots = [];
let nBallots;

if (window.innerWidth > 600) {
    nBallots = 27;
} else {
    nBallots = 12;
}

// Basic functions

function addOrRemoveReplacingButton() {
  let checkedBallots = ballots.filter(ballot => ballot.checked);
  if ((checkedBallots.length > 0) && 
  (!document.getElementById('replacer'))) {
    let replaceLast = document.createElement('input');
    replaceLast.value = 'Cambiar última';
    replaceLast.setAttribute('id', 'replacer');
    replaceLast.setAttribute('type', 'button');
    replaceLast.setAttribute('onclick', 'replaceLastBallot()');
    randomBallotSelector.parentNode.insertBefore(replaceLast, randomBallotSelector.nextSibling);
  } else if ((checkedBallots.length == 0) && (document.getElementById('replacer'))) {
    document.getElementById('replacer').remove();
  }
}

function modifyPrice() {
  let total = document.getElementById('total');
  total.innerText = ballots.filter(ballot => ballot.checked)
  .length * data.ballot_price;
}

function switchCheckedState(ballot) {
  ballots.forEach(generalBallot => {
    if (generalBallot.id == ballot.id) {
        generalBallot.checked = !ballot.checked;
    }
})
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
            'lottery_id': lotteryId
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

function removeBallotWrappers() {
    let ballotWrappers = document.querySelectorAll('.ballot-wrapper');
    ballotWrappers.forEach(wrapper => {
        wrapper.remove();
    })
}

function selectRandomBallot() {
  function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  if (ballots.filter(ballot => ballot.checked == false).length > 0) {
    let ballotIndex = getRandomInt(0, ballots.filter(ballot => ballot.checked == false).length-1);
    let selectedBallot = ballots.filter(ballot => ballot.checked == false)[ballotIndex];
    return selectedBallot;
  }
}


// Complex functions

function modifyPriceAndSwitchCheckedState(ballotId) {
  let ballot = ballots.filter(ballot => ballot.id == ballotId)[0];
  if (ballot.checked) {
    selectedBallots.shift();
  } else {
    selectedBallots.unshift(ballot);
  }
  switchCheckedState(ballot);
  modifyPrice();
  addOrRemoveReplacingButton();
}

function addOneRandomly() {
  let selectedBallot = selectRandomBallot();
  selectedBallots.unshift(selectedBallot);
  switchCheckedState(selectedBallot);
  modifyPrice();
  let ballotsToDisplay = ballots.filter(ballot => String(ballot.number)
  .includes(searchInput.value))
  .filter(ballot => !ballot.checked)
  .slice(0, nBallots-1);
  ballotsToDisplay.unshift(selectedBallot);
  addOrRemoveReplacingButton()
  removeBallotWrappers();
  appendBallots(ballotsToDisplay);
}

function replaceLastBallot() {
  selectedBallots[0].checked = false;
  selectedBallots.shift();
  let selectedBallot = selectRandomBallot();
  selectedBallots.unshift(selectedBallot);
  switchCheckedState(selectedBallot);
  modifyPrice();
  let ballotsToDisplay = ballots.filter(ballot => String(ballot.number)
  .includes(searchInput.value))
  .filter(ballot => !ballot.checked)
  .slice(0, nBallots-1);
  ballotsToDisplay.unshift(selectedBallot);
  addOrRemoveReplacingButton()
  removeBallotWrappers();
  appendBallots(ballotsToDisplay);
}

function submitForm() {
  removeBallotWrappers();
  appendBallots(ballots.filter(ballot => ballot.checked == true));
  document.getElementById('ballot-form').submit();
}

function filterAndAppendBallots() {
  removeBallotWrappers();
  let filteredBallots = ballots.filter(ballot => String(ballot.number)
  .includes(searchInput.value));
  appendBallots(filteredBallots.slice(0, nBallots));
}


// Bind functions to events

window.addEventListener('load', getBallotsFromBackend);

window.addEventListener('load', appendBallots(ballots.slice(0, nBallots)));

searchInput.addEventListener('keyup', filterAndAppendBallots);

randomBallotSelector.addEventListener('click', addOneRandomly);
