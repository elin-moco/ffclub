
$(document).ready(function(){

    var timeSpan = $('span.time');
    timeSpan.prettyDate();
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
    var eventPhotos = $('.eventPhotos');
    eventPhotos.masonry({
        'itemSelector': '.eventPhoto',
        columnWidth: 320,
        isAnimated: true
    });
    eventPhotos.infinitescroll({

            navSelector  : "#page-nav",
            // selector for the paged navigation (it will be hidden)
            nextSelector : "#page-nav a",
            // selector for the NEXT link (to page 2)
            itemSelector : ".eventPhoto"
            // selector for all items you'll retrieve
        },
        function(photos) {
            eventPhotos.masonry('appended', $(photos), true);
            timeSpan.prettyDate();
        });


});

