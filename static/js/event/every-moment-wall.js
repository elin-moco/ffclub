"use strict";


(function () {
    $('.eventPhoto').mouseover(function () {
        var url = $(this).find('a').attr('href');
        $('#fxos-phone-frame').show();
        $('#fxos-phone-frame').position({
            my: 'center',
            at: 'center',
            of: $(this),
            using: function (css) {
                $('#fxos-phone-frame').animate(css, 350);
            }
        });
        $('.bigShareButton').attr('data-url', url);
    });
    $('.bigShareButton').click(function () {
        FB.ui({
                method: 'feed',
                name: 'Facebook Dialogs',
                link: $(this).attr('data-url'),
                caption: 'Reference Documentation',
                description: 'Dialogs provide a simple, consistent interface for applications to interface with users.'
            },
            function (response) {
                if (response && response.post_id) {
                    alert('Post was published.');
                } else {
                    alert('Post was not published.');
                }
            }
        );
    });
})();