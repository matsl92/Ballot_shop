const searchInput = document.getElementById('search-input');
var nBallots;

if (window.innerWidth < 600) {
    nBallots = 12;
} else {
    nBallots = 40;
}

function appearBallots(ballots) {
    let i;
    for (i = 0; i < ballots.length; i++) {
        ballots[i].animate(
            [
                { transform: "translateY(100px)", opacity: 0},
                { opacity: 1}, 
            ], 
            {
                duration: 1000,
                iterations: 1,
                delay: i * 100
            }
        );
        ballots[i].style.opacity = 1;
    }
}

function myFunction() {
    if (Number(searchInput.value) || searchInput.value == '') {
        var filter, items, ballots, i, j, txtValue, matching, notMatching, orderedBallots;
        filter = searchInput.value;
        items = document.getElementById("items");
        ballots = items.getElementsByClassName("ballot-wrapper");
        matching = [];
        notMatching = []; 
        for (j = 0; j < ballots.length; j++) {
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
            orderedBallots[j].style.display = ''; 
            orderedBallots[j].style.order = j;
        }
        appearBallots(orderedBallots);
    };
}

searchInput.addEventListener('keyup', myFunction, false);