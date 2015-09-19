$(document).scroll(function() {
    $('#sticky-main-menu').css({display: $(this).scrollTop()>100 ? "block":"none"});
});