// function swapPages() {
//     dropdownAccount = document.getElementById('li-g-account');
//     dropdownBooking = document.getElementById('li-g-booking');
//     var accountPage = document.getElementsByClassName('pages-account');
//     var bookingPage = document.getElementsByClassName('pages-booking');
//     var pageTitle = document.getElementById('page-title');

//     document.getElementById("dropdown-list").addEventListener("click", function(e) {
//         // e.target will be the item that was clicked on
//         // e.target.style.color = "orange";

//         for (i = 0; i < bookingPage.length; i++) {
//             if (e.target == dropdownAccount) {
//                 pageTitle.innerText = "ACCOUNT"
//                 bookingPage[i].style.display = "none";
//                 accountPage[i].style.display = "initial";
//             }
    
//             if (e.target == dropdownBooking) {
//                 pageTitle.innerText = "BOOKING"
//                 bookingPage[i].style.display = "unset";
//                 accountPage[i].style.display = "none";
//             }
//         }
//     })
// }

const query = document.querySelectorAll('#cancelBookingBtn');
query.forEach((e) => {
    e.addEventListener('click', () => {
        const row = e.parentElement.parentElement; // clicked table row
        // var tr = row.getAttribute('name'); // clicked table row index name
        var td = row.lastElementChild; // get last element child, in this case its payment_id
        var paymentId = td.getAttribute('id'); // Get the payment id primary key

        // Check if the primary key last child is payment_id
        if (paymentId == 'payment_id') {
            var paymentIdValue = td.innerHTML;
            
            // Set the name of the confirm button to the primary key of a row
            const confirmCancel = document.getElementById('confirmCancellationBtn');
            confirmCancel.setAttribute('name', paymentId);
            confirmCancel.setAttribute('value', paymentIdValue);
        }
    });
});


const newPassword = document.getElementById('newPassword');
const confirmNewPassword = document.getElementById('confirmNewPassword');
newPassword.addEventListener('change', (e) => {
    if (e.target.value != '') {
        confirmNewPassword.required = false;
    }

    if (e.target.value == '') {
        confirmNewPassword.required = true;
    }
});