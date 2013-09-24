"use strict";


(function () {
    $('.eventPhoto').mouseover(function () {
        var url = $(this).find('a').attr('href');
        var caption = $(this).find('.photoDescription p').text();
        $('#fxos-phone-frame').show();
        $('#fxos-phone-frame').position({
            my: 'center',
            at: 'center',
            of: $(this),
            using: function (css) {
                $('#fxos-phone-frame').animate(css, 150);
            }
        });
        $('.bigShareButton').attr('data-url', url);
        $('.bigShareButton').attr('data-caption', caption);
    });
    $('.bigShareButton').click(function () {
        FB.ui({
                method: 'feed',
                name: 'Firefox OS 讓你盡情享受每一刻',
                link: $(this).attr('data-url'),
                caption: $(this).attr('data-caption'),
                description: '即日起，只要上傳自己生活中美好一刻的照片至活動網站與 Firefox OS 相框結合，並於投票期間廣邀親朋好友為自己投票衝人氣，就有機會獲得 Firefox OS 行動裝置等各項大獎！'
            },
            function (response) {
                if (response && response.post_id) {
                    alert('已成功分享至你的牆上');
                } else {
//                    alert('Post was not published.');
                }
            }
        );
    });

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
            eventPhotos.masonry('appended', $(photos), true);
        });

    var init_photo_actions = function (photos) {
        $(photos).find('.eventPhotoLink').click(
            function (e) {
                e.preventDefault();
                lightbox.show($(this).find('img').attr('data-large-src'));
            }
        );
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

})();