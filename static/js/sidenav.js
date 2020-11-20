$(document).ready(function() {
    var sideNavActiveLink = window.location.pathname.split("/")[1];
    $('#'+sideNavActiveLink).addClass('active-link');

    $("#headerToggle").click(function() { 
        $("#sideNav").toggleClass('show-nav');  // show navbar
        $("#headerToggle").toggleClass('bx-x');  // change icon
        $("#body").toggleClass('body-pd');  // add padding to body
        $("#header").toggleClass('body-pd');  // add padding to header
    });
});