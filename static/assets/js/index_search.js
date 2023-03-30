console.log('This is search!');

var nBallots;

if (window.innerWidth < 600) {
    nBallots = 12;
} else {
    nBallots = 8;
}

// function myFunction() {
//     var input, filter, items, ballots, i, j, txtValue;
//     input = document.getElementById("myInput");
//     filter = input.value;
//     items = document.getElementById("items");
//     ballots = items.getElementsByClassName("ballot-wrapper");
//     for (j = 0; j < ballots.length; j++) {
//         i = ballots[j].getElementsByTagName("i")[0];
//         txtValue = i.textContent || i.innerText;
//         if (txtValue.indexOf(filter) > -1) {
//             ballots[j].style.display = "";
//         } else {
//             ballots[j].style.display = "none";
//         }
//     }
// }



function myFunction() {
    var input, filter, items, ballots, i, j, txtValue, matching, notMatching, orderedBallots;
    input = document.getElementById("myInput");
    filter = input.value;
    items = document.getElementById("items");
    ballots = items.getElementsByClassName("ballot-wrapper");
    matching = [];
    notMatching = []; 
    for (j = 0; j < ballots.length; j++) {
        // ballots[j].style.color = 'white';
        ballots[j].style.display = 'none';
        i = ballots[j].getElementsByTagName("i")[0];
        txtValue = i.textContent || i.innerText;
        if (txtValue.indexOf(filter) > -1) {
            matching.push(ballots[j]);
        } else {
            notMatching.push(ballots[j]);
        }
    }
    orderedBallots = matching.concat(notMatching);
    for (j = 0; j < Math.min(orderedBallots.length, nBallots); j++) {
        orderedBallots[j].style.display = 'flex'; 
        orderedBallots[j].style.order = j;
    }
}