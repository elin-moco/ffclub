
$(document).ready(function(){

    var slideshow = new saw.Slideshow();
    $('.productPhotosLink').click(
        function(e) {
            e.preventDefault();
            slideshow.show($(this).attr('href'));
        }
    );
});
