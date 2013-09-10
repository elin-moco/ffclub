$(document).ready(function () {

    var popup = new Modal().Popup('.popup');
    if (popup.hasError()) {
        //Has validation errors
        popup.show();
    }
    $('.sharePhotoLink').click(function () {
        popup.show();
    });
    var authzHandler = function (response) {
        console.info(response);
        if (response.status === 'connected' || response.code) {
            var accessToken = response.code ? response.code : response.authResponse.accessToken;
            FB.api('/me/permissions', function (response) {
                if (response['data'][0]['publish_stream']) {
                    $('#fbToken').attr('value', accessToken);
                }
                else {
                    $('#shareOnFb').removeAttr('checked');
                }
            });
        } else {
            $('#shareOnFb').removeAttr('checked');
        }
    };
    $('#shareOnFb').click(function () {
        if (this.checked && FB) {
            FB.getLoginStatus(function (response) {
                if (response.status === 'connected') {
                    // the user is logged in and has authenticated your
                    // app, and response.authResponse supplies
                    // the user's ID, a valid access token, a signed
                    // request, and the time the access token
                    // and signed request each expire
                    var accessToken = response.authResponse.accessToken;
                    FB.api('/me/permissions', function (response) {
                        if (response['data'][0]['publish_stream']) {
                            $('#fbToken').attr('value', accessToken);
                        }
                        else {
                            FB.ui({
                                'method': 'permissions.request',
                                'perms': 'publish_stream',
                                'display': 'iframe' //THIS IS IMPORTANT TO PREVENT POPUP BLOCKER
                            }, authzHandler);
//                            FB.login(authzHandler, {'scope': 'publish_stream'});
                        }
                    });
                    //} else if (response.status === 'not_authorized') {
                    // the user is logged in to Facebook,
                    // but has not authenticated your app
                } else {
                    // the user isn't logged in to Facebook.
                    FB.login(authzHandler, {'scope': 'publish_stream'});
                }
            });
        }
    });

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
                gp.append('<div class="g-plusone" data-size="medium" data-href="' + url + '"></div>');
                gapi.plusone.go(gp.get(0));
            }
        }
    };


    var lightbox = new Modal().Lightbox('.eventPhotos');

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
            init_photo_actions(photos);
//            $(photos).on('mouseover', loadSocialButtons);
//            $(photos).find('.eventPhotoLink').click(function (e) {
//                e.preventDefault();
//                lightbox.show($(this).find('img').attr('data-large-src'));
//            });
//            $(photos).find('span.time').prettyDate();
//            $(photos).find('.removePhoto').on('click', function(e) {
//                e.preventDefault();
//            });
//            $(photos).find('.reportPhoto').on('click', function(e) {
//                e.preventDefault();
//            });
            eventPhotos.masonry('appended', $(photos), true);

        });

    var init_photo_actions = function (photos) {
        $(photos).find('span.time').prettyDate();
        $(photos).find('.eventPhotoLink').click(
            function (e) {
                e.preventDefault();
                lightbox.show($(this).find('img').attr('data-large-src'));
            }
        );
        $(photos).on('mouseover', loadSocialButtons);
        $(photos).find('.removePhoto').on('click', function (e) {
            e.preventDefault();
            var eventPhoto = $(this).closest('.eventPhoto');
            if (confirm('確定刪除？')) {
                $.ajax({
                    dataType: 'json',
                    url: $(this).attr('href')
                }).done(
                    function (response) {
                        if ('success' == response.result) {
                            eventPhotos.masonry('remove', eventPhoto);
                            eventPhotos.masonry('reload');
                        }
                        else {
                            alert(response.errorMessage);
                        }
                    }
                );
            }
        });
        $(photos).find('.reportPhoto').on('click', function (e) {
            e.preventDefault();
            $.ajax({
                dataType: 'json',
                url: $(this).attr('href')
            }).done(
                function (response) {
                    if ('success' == response.result) {
                        alert('感謝回報！我們會儘速處理。');
                    }
                    else {
                        alert(response.errorMessage);
                    }
                }
            );
        });
    };
    init_photo_actions(eventPhotos.find('.eventPhoto'));

});

