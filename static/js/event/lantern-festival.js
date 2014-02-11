"use strict";

(function () {
    var page_id = "229264713799595";
    var pageLiked = false;
    var subscriber = '';
    var randomPost = $('.myfx-post').eq(Math.floor((Math.random()*1000)%3));
    randomPost.css('display', 'block');
    var nextStage = function (next) {
        $('#steps').attr('class', 'step' + next);
        $.scrollTo('#fox-lantern');
        $('#sparkle').bind('animationend webkitAnimationEnd MSAnimationEnd oAnimationEnd', function () {
            var $steps = $('#steps');
            $steps.removeAttr('class');
            $('#fox-lantern').css('background', 'url(/static/img/event/lantern-festival/fox-' + next + '.png)');
            $steps.scrollTo('#step' + next, 1000, {axis: 'x'});
            $('#sparkle').unbind('animationend webkitAnimationEnd MSAnimationEnd oAnimationEnd');
        });
        if (4 == next) {
            $.get('/campaign/lantern-festival/claim/', {subscriber: subscriber}, function(response) {
                if ('claim_code' in response) {
                    $('#claim-code').text(response.claim_code);
                }
            });
        }
    };
    $('#login-fb').click(function () {
        if (pageLiked) {
            nextStage(2);
        }
        else {
            FB.login(function (response) {
                if (response && response.authResponse) {
                    var user_id = response.authResponse.userID;
                    var fql_query = "SELECT uid FROM page_fan WHERE page_id = " + page_id + "and uid=" + user_id;
                    FB.Data.query(fql_query).wait(function (rows) {
                        if (rows.length == 1 && rows[0].uid == user_id) {
                            nextStage(2);
                        }
                    });
                }
            }, {scope: 'user_likes'});
        }
    });
    window.fbAsyncInit = function () {
        FB.Event.subscribe('edge.create', function (response) {
            nextStage(2);
        });
        FB.getLoginStatus(function (response) {
            if (response && response.authResponse) {
                var user_id = response.authResponse.userID;
                var fql_query = "SELECT uid FROM page_fan WHERE page_id = " + page_id + "and uid=" + user_id;
                FB.Data.query(fql_query).wait(function (rows) {
                    if (rows.length == 1 && rows[0].uid == user_id) {
                        pageLiked = true;
//                        nextStage(2);
                    }
                });
            }
        });
    };
    /*
    var firstLoad = true;
    $('#subscription').load(function () {
        if (!firstLoad) {
            nextStage(3);
        }
        firstLoad = false;
    });
    */
    var eventMethod = window.addEventListener ? "addEventListener" : "attachEvent";
    var eventer = window[eventMethod];
    var messageEvent = eventMethod == "attachEvent" ? "onmessage" : "message";

    // Listen to message from child window
    eventer(messageEvent,function(e) {
        //run function//
        if (e.data) {
            var segments = e.data.split('=');
            if (segments.length == 2 && segments[0] == 'subscriber' && segments[1].indexOf('@') != -1) {
                subscriber = segments[1];
                nextStage(3);
            }
        }
    },false);
    $('#share-myfx').click(function () {
        FB.ui(
            {
                method: 'feed',
                link: randomPost.attr('href'),
            },
            function (response) {
                if (response && response.post_id) {
                    nextStage(4);
                }
            }
        );
    });
    $('#print-claim').click(function() {
        window.print();
    });

    $('#fox-lantern').click(function(e) {
        if (e.target == this) {
            page('/campaign/lantern-festival/firefox-lantern/');
        }
    });
    $('#popup').click(function(e) {
        if (e.target == this) {
            page('/campaign/lantern-festival/');
        }
    });

    $('.share-button').click(function() {
        if (FB) {
            FB.ui({
                method: 'feed',
                link: window.location.origin+'/campaign/lantern-festival/firefox-lantern/',
                picture: window.location.origin+$('#fox-lantern-large').attr('src'),
                name: 'Firefox 元宵點燈',
                caption: '在充滿活力朝氣的馬年，Mozilla 為了感謝使用者的支持，邀請您進一步用行動加入打造網路光明未來的行列。',
                description: '請依步驟點亮 Firefox 火狐燈籠，為新的一年衝個吉利好彩頭，狐狐生風！'
            }, function(response) {
            });
        }
    });
    var hidePopup = function() {
        $('#popup').hide();
    };

    var showPopup = function() {
        $('#popup').show();
    };

    page('/campaign/lantern-festival/', hidePopup);
    page('/campaign/lantern-festival/firefox-lantern/', showPopup);
    page();
})();