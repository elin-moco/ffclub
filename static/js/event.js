$(document).ready(function () {

    var loadSocialButtons = function () {
        if (FB && gapi) {
            var url = $(this).find('a.eventPhotoLink').attr('href');
            var fb = $(this).find('div.facebookLike');
            var gp = $(this).find('div.googlePlus');
            if (fb.children().length == 0) {
                fb.append('<div class="fb-like" data-send="false"' +
                    'data-href="' + url + '"' +
                    'data-layout="button_count" data-width="150" data-show-faces="false"></div>');
                FB.XFBML.parse(fb.get(0));
            }
            if (gp.children().length == 0) {
                gp.append('<div class="g-plusone" data-size="medium" data-href="'+url+'"></div>');
                gapi.plusone.go(gp.get(0));
            }
        }
    };

    var timeSpan = $('span.time');
    timeSpan.prettyDate();
    var lightbox = new Modal().Lightbox('.eventWall');
    $('.eventPhotoLink').click(
        function (e) {
            e.preventDefault();
            lightbox.show($(this).find('img').attr('data-large-src'));
        }
    );
    var popup = new Modal().Popup('.popup');
    $('.sharePhotoLink').click(function () {
        popup.show();
    });
    var eventPhotos = $('.eventPhotos');
    eventPhotos.masonry({
        'itemSelector': '.eventPhoto',
        columnWidth: 320,
        isAnimated: true
    });
    eventPhotos.infinitescroll({
            navSelector: '#page-nav',
            // selector for the paged navigation (it will be hidden)
            nextSelector: '#page-nav a',
            // selector for the NEXT link (to page 2)
            itemSelector: '.eventPhoto',
            // selector for all items you'll retrieve
            loadingImg: '',
            loadingText: '',
            donetext: '',
            animate: true
        },
        function (photos) {
            $(photos).on('mouseover', loadSocialButtons);
            $(photos).find('.eventPhotoLink').click(function (e) {
                e.preventDefault();
                lightbox.show($(this).find('img').attr('data-large-src'));
            });
            $(photos).find('span.time').prettyDate();
            eventPhotos.masonry('appended', $(photos), true);

        });
    var eventPhoto = $('.eventPhoto');
    eventPhoto.on('mouseover', loadSocialButtons);
});

