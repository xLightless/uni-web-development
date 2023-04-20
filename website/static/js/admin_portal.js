
// On page load update the date
window.onload = function() {
    let date = new Date();
    const month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const day = [ "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    document.getElementById('update-todays-date').innerHTML = day[date.getDay()] + ', ' + date.getDate() + ' ' + month[date.getMonth()] + ' ' + date.getFullYear();
}

// var xMonthsOfYear = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
// var yMonthlySalesData = [10, 20, 30, 55, 80, 11, 39, 99, 999, 1233, 30, 250];

// var data = [{
//     x:xMonthsOfYear,
//     y:yMonthlySalesData,
//     type:"bar"
// }];

// var layout = {title:"Net Sales Per Month"};
// var config = {responsive: true}

// Plotly.newPlot("monthlySalesChart", data, layout, config);