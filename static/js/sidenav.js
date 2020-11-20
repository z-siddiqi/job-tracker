$(document).ready(function() {
    $("#headerToggle").click(function() { 
        $("#sideNav").toggleClass('show-nav');  // show navbar
        $("#headerToggle").toggleClass('bx-x');  // change icon
        $("#body").toggleClass('body-pd');  // add padding to body
        $("#header").toggleClass('body-pd');  // add padding to header
    });
    
    $(".side-nav-link").click(function() {
        $(".cust-active").each(function() {
            $(this).removeClass('cust-active');
        });

        $(this).addClass('cust-active');
      });
});