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