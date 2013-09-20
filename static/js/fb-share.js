"use strict";

(function () {
    var authzHandler = function (response) {
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
})();