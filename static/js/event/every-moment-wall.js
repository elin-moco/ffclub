"use strict";


(function () {
    $('.bigShareButton').click(function () {
        FB.ui({
                method: 'feed',
                name: 'Firefox OS 讓你盡情享受每一刻',
                link: $(this).attr('data-url'),
                caption: $(this).attr('data-caption'),
                description: '這是屬於我的美好時刻，跟 Firefox OS 完美結合耶！活動很簡單，只要上傳自己生活中美好一刻的照片至活動網站與 Firefox OS 相框結合，在投票期間請好友為自己投票，就有機會獲得 Firefox OS 手機…！'
            },
            function (response) {
                if (response && response.post_id) {
                    alert('已成功分享至你的牆上');
                }
            }
        );
    });
    $('.bigVoteButton').click(function () {
        var $voteButton = $(this);
        var voteUrl = $(this).attr('data-url');
        if (voteUrl) {
            $.ajax({
                dataType: 'json',
                url: voteUrl
            }).done(function (response) {
                    if ('success' == response.result) {
                        var $photo = $('#'+$voteButton.attr('data-id'));
                        var voteCount = 1 + parseInt($photo.attr('data-vote-count'));
                        $photo.attr('data-vote-count', voteCount);
                        $photo.attr('data-voted', 'True');
                        $('.voteCount em').text(voteCount);
                        $voteButton.css('opacity', 0.5);
                        $voteButton.css('pointer-events', 'none');
                        var fb_sync_action = function() {
                            var fb_publish_action = function() {
                                FB.api('/me/' + $voteButton.attr('fb-namespace') + ':vote',
                                    'post', {picture: $photo.find('.eventPhotoLink').attr('href')},
                                    function(response) {
                                       console.info(response);
                                       if (!response || response.error) {
                                          alert('同步 Facebook 發生問題');
                                       } else {
                                          alert('同步成功！');
                                       }
                                    }
                                )
                            };
                            FB.getLoginStatus(function (response) {
                                if (response.status === 'connected') {
                                    fb_publish_action();
                                } else {
                                    // the user isn't logged in to Facebook.
                                    FB.login(function(response) {
                                        if (response.status === 'connected') {
                                            fb_publish_action();
                                        }
                                    });
                                }
                            });
                        };
                        $('#vote-confirm-dialog').dialog({
                            resizable:false,
                            modal:true,
                            buttons: {
                                '確定': function() {
                                    fb_sync_action();
                                    $(this).dialog('close');
                                },
                                '取消': function() {
                                    $(this).dialog('close');
                                }
                            }
                        });
                    }
                    else {
                        alert(response.errorMessage);
                    }
                }
            );
        }
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
        $(photos).mouseover(function () {
            var url = $(this).find('a').attr('href');
            var caption = $(this).find('.photoDescription p').text();
            var voteUrl = $(this).find('.votePhoto').attr('href');
            $('#fxos-phone-frame').show();
            $('#fxos-phone-frame').position({
                my: 'center',
                at: 'center',
                of: $(this),
                using: function (css) {
                    $('#fxos-phone-frame').animate(css, 150);
                }
            });
            $('.voteCount').css('right', -60);
            $(this).find('.voteCount').css('right', -68);
            $('.bigShareButton').attr('data-url', url);
            $('.bigShareButton').attr('data-caption', caption);
            $('.bigVoteButton').attr('data-url', voteUrl);
            $('.bigVoteButton').attr('data-id', $(this).attr('id'));
            if (!voteUrl || $(this).attr('data-voted') == 'True') {
                $('.bigVoteButton').css('opacity', 0.5);
                $('.bigVoteButton').css('pointer-events', 'none');
            }
            else {
                $('.bigVoteButton').css('opacity', 1);
                $('.bigVoteButton').css('pointer-events', 'auto');
            }
        });
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