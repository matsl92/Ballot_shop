// const searchInput = document.getElementById('search-input');
// const ballotId = document.
const lotteryId = 2;

const searchInput = document.getElementById('search-input');

let nBallots;

if (window.innerWidth > 600) {
    nBallots = 30;
} else {
    nBallots = 12;
}

// PRODUCTION

// const ballotFetchURL = 'https://web-production-31f8.up.railway.app/fetch_ballots/';


// LOCALHOST

const ballotFetchURL = 'http://127.0.0.1:8000/fetch_ballots/';



var ballots = [];


function appendBallots(ballots) {
    var items, ballotWrapper, iconDiv, input, label, I;
    items = document.getElementById('items');
    
    for (let i = 0; i < ballots.length; i++) {
        ballotWrapper = document.createElement('div');
        ballotWrapper.classList.add('ballot-wrapper', 'col-auto', 'icon-box');
        ballotWrapper.setAttribute("data-aos", "fade-up");  // don't forget about data-aos-delay with the for loop

        iconDiv = document.createElement('div');
        iconDiv.classList.add('icon');

        input = document.createElement('input');
        input.classList.add('balota-input');
        input.setAttribute("type", "checkbox");
        input.setAttribute("name", "id");
        input.setAttribute("onclick", "modifyPrice()");  // set value and id attributes with a for loop

        label = document.createElement('label');
        label.classList.add("balota-label", "icon")  // set attribute for with a for loop

        I = document.createElement('i');
        I.classList.add('bi'); // set innerText with ballot.number 

        // Add varibales

        I.innerText = String(ballots[i].number);

        label.setAttribute("for", String(ballots[i].id));

        input.setAttribute("value", String(ballots[i].id));
        input.setAttribute("id", String(ballots[i].id));

        ballotWrapper.setAttribute("data-aos-delay", String(i*100));

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

        for (let i = 0; i < data.ballots.length; i++) {
            ballots.push(data.ballots[i]);
        }

        appendBallots(ballots.slice(0, nBallots));

        
    })
}


window.addEventListener('load', getBallotsFromBackend);


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