console.log('This is search!');

function myFunction() {
    var input, filter, items, ballots, i, j, txtValue;
    input = document.getElementById("myInput");
    filter = input.value;
    items = document.getElementById("items");
    ballots = items.getElementsByClassName("ballot-wrapper");
    for (j = 0; j < ballots.length; j++) {
        i = ballots[j].getElementsByTagName("i")[0];
        txtValue = i.textContent || i.innerText;
        if (txtValue.indexOf(filter) > -1) {
            ballots[j].style.display = "";
        } else {
            ballots[j].style.display = "none";
        }
    }
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



// function myFunction() {
//     var input, filter, ul, li, a, i, txtValue;
//     input = document.getElementById("myInput");
//     filter = input.value.toUpperCase();
//     ul = document.getElementById("myUL");
//     li = ul.getElementsByTagName("li");
//     for (i = 0; i < li.length; i++) {
//         a = li[i].getElementsByTagName("a")[0];
//         txtValue = a.textContent || a.innerText;
//         if (txtValue.toUpperCase().indexOf(filter) > -1) {
//             li[i].style.display = "";
//         } else {
//             li[i].style.display = "none";
//         }
//     }
// }