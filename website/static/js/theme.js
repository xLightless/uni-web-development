

// BASE CLASS JAVASCRIPT FILE

var width;
var height;

var leaving = document.getElementById('booking-leaving');
var returning = document.getElementById('booking-return');
var basket = document.getElementById('booking-basket');
var grid = document.getElementsByClassName('container-booking-grid');


// Resize event to check browser window width and height
window.addEventListener('resize', () => {
    var w = document.documentElement.clientWidth;
    var h = document.documentElement.clientHeight;

    width = w
    height = h

    // // Min-width
    if (width >= 1366) {
        var sidebar = document.getElementsByClassName("grid-sidebar")
        for (i = 0; i < sidebar.length; i++) {
        sidebar[i].style.display = "block"
        sidebar[i].style.width = "200px"
        }
        document.getElementById('overlay-backdrop').style.display = "none"
    
        // if (window.getComputedStyle(leaving).display !== "none") {
        //     basket.style.display = "initial";
        // }
    }

    // Max-width
    if (width <= 1365) {
        if (document.getElementById('overlay-backdrop').style.display == "none") {
            var sidebar = document.getElementsByClassName("grid-sidebar")
            console.log("backdrop is none")
            for (i = 0; i < sidebar.length; i++) {
                sidebar[i].style.display = "none"
            }
        }
        basket.style.display = "none";
    }
})

// BASE THEME JS

function toggleNavbar() {
    var sidebar = document.getElementsByClassName('grid-sidebar')

    // Checks if user clicks outside or inside sidebar/nav toggle-navbar
    window.addEventListener('click', function(e){
        if (document.getElementById('toggle-navbar').contains(e.target)) {
            // Expand sidebar if mouse clicks toggle-navbar
            for (i = 0; i < sidebar.length; i++) {
                // Update sidebar
                sidebar[i].style.display = "initial"
                sidebar[i].style.width = "200px"
                sidebar[i].style.animation = "fade-in 0.4s"

                // Grayscale page content
                this.document.getElementById('overlay-backdrop').style.display = "block"
                this.document.getElementById('overlay-backdrop').style.width = 'calc(100% - 200px)'
                this.document.getElementById('overlay-backdrop').style.left = "200px"
                this.document.getElementById('overlay-backdrop').style.animation = "fade-in 0.4s"
            }

        } else {
            // If mouse outside toggle-navbar then it must be on sidebar else none
            // if (document.getElementById('sidebar').contains(e.target)){
            //     console.log("inside  sidebar")

            //     } else {

            //     // If mouse outside sidebar when  clicking then sidebar must be closed
            //     for (i = 0; i < sidebar.length; i++) {
            //         sidebar[i].style.display = "none"
            //         document.getElementById('overlay-backdrop').style.display = "none"

            //     }
            // }

            if (!document.getElementById('sidebar').contains(e.target)){
                console.log("inside sidebar")
                // If mouse outside sidebar when  clicking then sidebar must be closed
                for (i = 0; i < sidebar.length; i++) {
                    sidebar[i].style.display = "none"
                    document.getElementById('overlay-backdrop').style.display = "none"

                }
            } else {

                // Inside sidebar

            }
        }

        if (!document.getElementById('toggle-navbar').contains(e.target)) {
            if (width >= 1366) {
                for (i = 0; i < sidebar.length; i++) {
                    sidebar[i].style.display = "block"
                    sidebar[i].style.width = "200px"
                }
            }
        }


    });
}

// LOGIN PAGE JS

var login = document.getElementById('login');
var password = document.getElementById('forgot-password');

function passwordContainer() {
    // Change page content container to forgot password
    login.style.display = 'none';
    password.style.display = 'initial';
    var email = document.getElementById('loginEmail').value;
    reset = document.getElementById('resetEmail').value = email
}

function loginContainer() {
    // Changes page content container to login container
    login.style.display = 'initial';
    password.style.display = 'none';
}

// ACCOUNT PAGE JS

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

// PUBLIC BOOKING PAGE JS

function toggleBookingContainers() {

    let w = window.innerWidth;
    console.log(w)
    

    if (w > 1366) {
        leaving.style.display = "unset";
        // leaving.style.animation = "js-page-fade-in 5s";
        returning.style.display = "unset";
        // returning.style.animation = "js-page-fade-in 2s";
        basket.style.display = "unset";
        // basket.style.animation = "js-page-fade-in 2s";
    }

    // medium screen
    if (w > 576 && w < 1366) {
        leaving.style.display = "unset";
        // leaving.style.animation = "js-page-fade-in 2s";
        returning.style.display = "unset";
        // returning.style.animation = "js-page-fade-in 2s";
    }
}

function getFormValues() {
    var search_inputs = document.getElementsByTagName('input');
    for (i = 0; i < search_inputs.length; i++) {
        if (search_inputs[i].value == "") {
            search_inputs[i].style.border = "2px solid red";
        }

        if (search_inputs[i].value != "") {
            search_inputs[i].style.border = "unset";
        }
    }
}


function buttonClickEvent(buttonID, eventID) {
    var btn = document.getElementById(buttonID);
    var event = document.getElementById(eventID)

    document.addEventListener('click', function(e) {
        if (e.target == btn) {
            event.style.display = "unset";
        }
    })
}


// Location inputs

let location_input = document.querySelector('location');
let destination_input = document.querySelector('destination');

let dropdown_values = document.getElementById('dropdown-search');

location_input.addEventListener('input', updateSearchValues);

function updateSearchValues(e) {
    // Display dropdown box below input element and updates as user types a value
    dropdown_values.textContent = e.target.value;
}


// INDEX PAGE JS

const departure = document.getElementById('departure');
const departContainer = document.getElementById('depart-container');
departure.addEventListener('focus', () => {
    departContainer.classList.add('active');
});
departure.addEventListener('blur', () => {
    departContainer.classList.remove('active');
});