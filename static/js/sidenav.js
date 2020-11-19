$(document).ready(function() {
    $("#headerToggle").click(function() { 
        $("#sideNav").toggleClass('show');  // show navbar
        $("#headerToggle").toggleClass('bx-x');  // change icon
        $("#body").toggleClass('body-pd');  // add padding to body
        $("#header").toggleClass('body-pd');  // add padding to header
    });
    
    $(".nav-link").click(function() {
        $(".active").each(function() {
            $(this).removeClass('active');
        });

        $(this).addClass('active');
      });
});