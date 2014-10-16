"use strict";

(function () {
    var loginHandler = function () {
        var fbpile = $('div.fbpile');
        if (fbpile.children().length == 0) {
            fbpile.append('<div class="fb-facepile" data-app-id="' + fbpile.attr('data-app-id') + '" data-max-rows="1"></div>');
            FB.XFBML.parse(fbpile.get(0));
        }
        //Notify popup opener if FB login success
        if (window.opener) {
            FB.getLoginStatus(function(response) {
                if (response.status === 'connected') {
                    window.opener.loginSuccess();
                    window.close();
                }
            });
        }
    };
    window.loginSuccess = function() {
        $('.loginBox').hide();
        //Notify embedding parent if FB login success
        if (window.parent) {
          window.parent.postMessage('login=success', '*');
        }
    };
    window.fbAsyncInit = loginHandler;
    $('.facebook-login').click(function(e) {
        e.preventDefault();
        window.open($(this).attr('href'), 'Facebook 登入', 'menubar=0,location=1,resizable=1,scrollbars=1,status=0,width=700,height=375');
    });
})();