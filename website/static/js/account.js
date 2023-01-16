function swapPages() {
    dropdownAccount = document.getElementById('li-g-account');
    dropdownBooking = document.getElementById('li-g-booking');
    var accountPage = document.getElementsByClassName('pages-account');
    var bookingPage = document.getElementsByClassName('pages-booking');
    var pageTitle = document.getElementById('page-title');

    document.getElementById("dropdown-list").addEventListener("click", function(e) {
        // e.target will be the item that was clicked on
        // e.target.style.color = "orange";

        for (i = 0; i < bookingPage.length; i++) {
            if (e.target == dropdownAccount) {
                pageTitle.innerText = "ACCOUNT"
                bookingPage[i].style.display = "none";
                accountPage[i].style.display = "initial";
            }
    
            if (e.target == dropdownBooking) {
                pageTitle.innerText = "BOOKING"
                bookingPage[i].style.display = "unset";
                accountPage[i].style.display = "none";
            }
        }
    })
}