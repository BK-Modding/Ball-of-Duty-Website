$(document).ready(function() {
    $('.parallax').parallax();
    $('select').material_select();
    $('ul.tabs').tabs();
    $('.collapsible').collapsible();
    $('select').material_select();
    $('.carousel').carousel();
    $('.slider').slider({
          full_width: false,
          interval: 5000,
          transition: 800,
          });
});
$('a[href^="#"]').on('click', function(e) {
    e.preventDefault();

    var target = this.hash;
    if (target != "#questions1" && target != "#questions2" && target != "#questions3" && target != "#dates" && target != "#terms") {
        var $target = $(target);

        $('html, body').stop().animate({
            'scrollTop': $target.offset().top - 75
        }, 900, 'swing', function() {
            window.location.hash = target;
        });
    }

});
