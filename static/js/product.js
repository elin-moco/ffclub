
$(document).ready(function(){

    var slideshow = new Modal().Slideshow();
    $('.productPhotosLink').click(
        function(e) {
            e.preventDefault();
            slideshow.show($(this).attr('href'));
        }
    );
});
