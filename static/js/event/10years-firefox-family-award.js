"use strict";

(function () {
    var loginPopup = new Modal().Popup('.loginPopup');
    var loginHandler = function () {
        var title = '登入 Firefox 俱樂部';
        if ($(this).attr('title')) {
            title = $(this).attr('title');
        }
        loginPopup.show(title);
        var fbpile = $('div.fbpile');
        if (fbpile.children().length == 0) {
            fbpile.append('<div class="fb-facepile" data-app-id="' + fbpile.attr('data-app-id') +
                    '" data-action="Comma separated list of action of action types" data-width="400" data-max-rows="1"></div>');
            FB.XFBML.parse(fbpile.get(0));
        }
        if (window.opener) {
            FB.getLoginStatus(function(response) {
                if (response.status === 'connected') {
                    window.opener.loginSuccess();
                    window.close();
                }
                else {

                }
            });
        }
    };
    window.loginSuccess = function() {
        loginPopup.hide();
    };
    window.fbAsyncInit = loginHandler;
    $('.facebook-login').click(function(e) {
        e.preventDefault();
        window.open($(this).attr('href'), 'Facebook 登入', 'menubar=0,location=1,resizable=1,scrollbars=1,status=0,width=700,height=375');
    });
})();