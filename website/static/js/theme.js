

// BASE CLASS JAVASCRIPT FILE

var width;
var height;

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
        // basket.style.display = "none";
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
        returning.style.display = "unset";
        basket.style.display = "unset";
    }

    // medium screen
    if (w > 576 && w < 1366) {
        leaving.style.display = "unset";
        returning.style.display = "unset";
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

// INDEX PAGE JS

var backdrop = document.getElementById('overlay-backdrop');

function pageSelector(pageToDisplay, targetID) {
    let page = document.getElementById(pageToDisplay);
    let targets = document.getElementById(targetID);
    let removeButton = document.getElementById('btn-datetime-remove');
    let removeButtonLabel = document.getElementById('label-datetime-remove');

    targets.addEventListener("click", function(e) {
        if (e.target == removeButton || e.target == removeButtonLabel) {
            e.stopPropagation();
            e.preventDefault();
            console.log("Removing return tickets and datetime.");
        }
        else {
            page.style.display = "block";
            backdrop.style.display = "block";
        }
    });
}

function pageReturn(buttonID, eventID) {
    // Returns the user to the previous page
    var btn = document.getElementById(buttonID);
    var event = document.getElementById(eventID)

    document.addEventListener('click', function(e) {
        if (e.target == btn) {
            event.style.display = "none";
            backdrop.style.display = "none";
        }
    })
}

function swingRadios() {
    // Used to swap between Radio inputs
    let swingRadios = document.getElementById('swing-radios');
    let returnRadio = document.getElementById('params-traveller-return');
    let onewayRadio = document.getElementById('params-traveller-oneway');

    let swingChildren = swingRadios.childNodes;


    for (i = 0; i<swingChildren.length; i++) {
        swingChildren[i].addEventListener("click", (e) => {
            if (e.target == onewayRadio) {
                returnRadio.checked = false;
            }

            if (e.target == returnRadio) {
                onewayRadio.checked = false;
            }

        });
    }

}