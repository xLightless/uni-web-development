
// On page load update the date
window.onload = function() {
    let date = new Date();
    const month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const day = [ "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    document.getElementById('update-todays-date').innerHTML = day[date.getDay()] + ', ' + date.getDay() + ' ' + month[date.getMonth()] + ' ' + date.getFullYear();
}