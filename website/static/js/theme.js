
// BASE CLASS JS FILE

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
            // console.log("backdrop is none")
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
                // console.log("inside sidebar")
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
    // console.log(w)
    

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

var removeButton = document.getElementById('btn-datetime-remove');
removeButton.addEventListener('click', removeReturnDate);

function removeReturnDate() {
    // Return remove button functionality
    // let removeButton = document.getElementById('btn-datetime-remove');

    // removeButton.addEventListener('click', (e) => {
        
    // })

    let returnLabel = document.getElementById('label-swing-to');
    if (returnLabel.innerText != "No return added") {
        returnLabel.innerText = "No return added."
        returnDate.value = "";
    }

    // if (returnDate.value = "") {
    //     returnDate.value = "";

    // }

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

        // Only return if data is entered
        // if (e.target == document.getElementById("btn-confirmation-swing")) {
        //     console.log("btn swing clicked.")

        //     if (!departDate.value) {
        //         departDate.style.borderColor = "3px solid red";
        //     } else {
        //         departDate.style.border = "initial";
        //     }
        // }
    })
}

function swingRadios() {
    // Used to swap between Radio inputs
    let swingRadios = document.getElementById('swing-radios');
    let returnRadio = document.getElementById('params-traveller-return');
    let onewayRadio = document.getElementById('params-traveller-oneway');

    let swingChildren = swingRadios.childNodes;


    for (i = 0; i < swingChildren.length; i++) {
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

function removeReturnOptions() {
    const btnReturnRemove = document.getElementById('btn-datetime-remove');
    const lblReturnValue = document.getElementById('label-swing-to');
    btnReturnRemove.addEventListener('click', () => {
        lblReturnValue.innerText = "No return added.";
    });
}

// Sets datepicker min date to todays date
date = new Date();
var minDate = date.toISOString().split('T')[0];
document.getElementsByName("swing-from-datepicker")[0].setAttribute('min', minDate);
returnInput = document.getElementsByName("swing-to-datepicker")[0].setAttribute('min', minDate);

// Get input fields by ID
var departDate = document.getElementById('depart-date');
var returnDate = document.getElementById('return-date');

// Add a updating listener to datepicker
departDate.addEventListener('change', updateDepartValue);
returnDate.addEventListener('change', updateReturnValue);

function updateDepartValue() {
    // Event listener function to handle updating input values

    // If return date is empty OR not return date not equal to depart date update values
    if ((!returnDate.value) || (returnDate.value != departDate.value)) {
        console.log("Updating Swing Parameters.")
        newReturnVal = departDate.value;
        returnDate.value = newReturnVal;
    }
    
    let returnLabel = document.getElementById('label-swing-to');
    let departLabel = document.getElementById('label-swing-from');
    let updateReturnDate = new Date(returnDate.value);
    returnLabel.innerText = updateReturnDate.toDateString();

    let departDepartDate = new Date(departDate.value);
    departLabel.innerText = departDepartDate.toDateString();
}

function updateReturnValue() {
    /*
        Updates the maximum length of days based on the user departure selection.    
    */

    let date = new Date(departDate.value);
    let minDate = new Date(date.setDate(date.getDay() + 19)).toISOString().split('T')[0]; // Prevents user clicking a day before their selected day
    let maxDate = new Date(date.setDate(date.getDay() + 109)).toISOString().split('T')[0]; // Prevents user clicking past the selection days
    document.getElementsByName("swing-to-datepicker")[0].setAttribute('min', minDate);
    document.getElementsByName("swing-to-datepicker")[0].setAttribute('max', maxDate);

    let returnLabel = document.getElementById('label-swing-to');
    let departLabel = document.getElementById('label-swing-from');
    let updateReturnDate = new Date(returnDate.value);
    returnLabel.innerText = updateReturnDate.toDateString();

    let departDepartDate = new Date(departDate.value);
    departLabel.innerText = departDepartDate.toDateString();
    let newReturnLabel = returnDate.value;
    returnLabel.innerText = newReturnLabel.toDateString();
}



function locationsConfirmButtonEvent() {
    let inputFrom = document.getElementById('input-box-from');
    let inputTo = document.getElementById('input-box-to');
    if ((inputFrom.value != "" && inputTo.value != "") && (inputFrom.value != inputTo.value)) {
        pageReturn('btn-confirmation-locations', 'page-locations');

        let locationFrom = document.getElementById('label-location-from');
        let locationTo = document.getElementById('label-location-to');

        locationFrom.innerText = inputFrom.value;
        locationTo.innerText = inputTo.value;
    }
}

function swingConfirmButtonEvent() {
    let inputDepart = document.getElementById('depart-date');
    let inputReturn = document.getElementById('return-date');
    let selectPassengers = document.getElementById('passengers-amount');
    let selectSeatClass = document.getElementById('seat-class-type');

    // if (inputDepart.value != "" && selectPassengers.value != "" && selectSeatClass != "") {
    //     pageReturn('btn-confirmation-swing', 'page-swing');
    // }

    // pageReturn('btn-confirmation-swing', 'page-swing');
    if (departDate.value != "" && selectPassengers.value != "" && selectSeatClass != "") {
        pageReturn('btn-confirmation-swing', 'page-swing');

        let passengers = document.getElementById('label-swing-people');
        let seatType = document.getElementById('label-swing-seat-type');

        passengers.innerText = selectPassengers.value;
        seatType.innerText = selectSeatClass.value;



        

    }


}