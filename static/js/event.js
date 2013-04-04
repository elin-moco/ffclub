
$(document).ready(function(){

    var lightbox = new saw.Lightbox('.eventWall');
    $('.eventPhotoLink').click(
        function(e) {
            e.preventDefault();
            lightbox.show($(this).attr('href'));
        }
    );
    var popup = new saw.Popup('.popup');
    $('.sharePhotoLink').click(function() {
        popup.show();
    });
});

$('.eventWall').imagesLoaded(
    function() {
        $(this).masonry({
            'itemSelector': '.eventPhoto',
            columnWidth: 320,
            isAnimated: true
        });
    }
);
$('span.time').prettyDate();