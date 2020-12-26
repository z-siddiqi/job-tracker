$(document).ready(function () {
    var sideNavActiveLink = window.location.pathname.split("/")[1];
    $("#" + sideNavActiveLink).addClass('active-link');

    $("#appHeaderToggle").click(function () {
        $("#sideBar").toggleClass('show-nav');  // show navbar
        $("#appHeaderToggle").toggleClass('bx-x');  // change icon
        $("body").toggleClass('body-pd');  // add padding to body
        $("#appHeader").toggleClass('body-pd');  // add padding to header
    });
});