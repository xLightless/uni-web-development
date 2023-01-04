

// base class theme js

var width;
var height;

// Resize event to check browser window width and height
window.addEventListener('resize', () => {
    var w = document.documentElement.clientWidth;
    var h = document.documentElement.clientHeight;

    width = w
    height = h

    // // Min-width
    if (width >= 768) {
        var sidebar = document.getElementsByClassName("grid-sidebar")
        for (i = 0; i < sidebar.length; i++) {
        sidebar[i].style.display = "block"
        sidebar[i].style.width = "200px"
        }
        document.getElementById('overlay-backdrop').style.display = "none"
    }

    // Max-width
    if (width <= 767) {
        if (document.getElementById('overlay-backdrop').style.display == "none") {
            var sidebar = document.getElementsByClassName("grid-sidebar")
            console.log("backdrop is none")
            for (i = 0; i < sidebar.length; i++) {
                sidebar[i].style.display = "none"
            }
        }
    }
})

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

                // Grayscale page content
                this.document.getElementById('overlay-backdrop').style.display = "block"
                this.document.getElementById('overlay-backdrop').style.width = 'calc(100% - 200px)'
                this.document.getElementById('overlay-backdrop').style.left = "200px"
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
            if (width >= 768) {
                for (i = 0; i < sidebar.length; i++) {
                    sidebar[i].style.display = "block"
                    sidebar[i].style.width = "200px"
                }
            }
        }


    });
}