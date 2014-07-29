"use strict";

function gaTrack(eventArray, callback) {
    // submit eventArray to GA and call callback only after tracking has
    // been sent, or if sending fails.
    //
    // callback is optional.
    //
    // Example usage:
    //
    // $(function() {
    //      var handler = function(e) {
    //           var _this = this;
    //           e.preventDefault();
    //           $(_this).off('submit', handler);
    //           gaTrack(
    //              ['_trackEvent', 'Newsletter Registration', 'submit', newsletter],
    //              function() {$(_this).submit();}
    //           );
    //      };
    //      $(thing).on('submit', handler);
    // });
    var timer = null;
    var hasCallback = typeof(callback) === 'function';
    var gaCallback;

    // Only build new function if callback exists.
    if (hasCallback) {
        gaCallback = function() {
            clearTimeout(timer);
            callback();
        };
    }
    // console.info(eventArray);
    if (typeof(window._gaq) === 'object') {
        // send event to GA
        window._gaq.push(eventArray);
        // Only set up timer and hitCallback if a callback exists.
        if (hasCallback) {
            // Failsafe - be sure we do the callback in a half-second
            // even if GA isn't able to send in our trackEvent.
            timer = setTimeout(gaCallback, 500);

            // But ordinarily, we get GA to call us back immediately after
            // it finishes sending our things.
            // https://developers.google.com/analytics/devguides/collection/gajs/#PushingFunctions
            // This is called after GA has sent the current pending data:
            window._gaq.push(gaCallback);
        }
    } else {
        // GA disabled or blocked or something, make sure we still
        // call the caller's callback:
        if (hasCallback) {
            callback();
        }
    }
}

(function () {
    var page_id = "229264713799595";
    var pageLiked = false;
    var subscriber = '';
    var randomPost = $('.myfx-post').eq(Math.floor((Math.random()*1000)%3));
    randomPost.css('display', 'block');
    var randomVideo = $('.myfx-video').eq(Math.floor((Math.random()*1000)%3));
    randomVideo.css('display', 'block');

    $(document).keydown(function(e) {
        switch(e.keyCode) {
            case 49:
                $('.pyro').hide();
                $('#hearts').attr('class', '');
                nextStage(0);
                break;
            case 50:
                $('.pyro').hide();
                $('#hearts').attr('class', '');
                nextStage(1);
                break;
            case 51:
                $('.pyro').hide();
                $('#hearts').attr('class', '');
                nextStage(2);
                break;
            case 52:
                $('.pyro').hide();
                nextStage(3);
                break;
            case 53:
                nextStage(4);
                break;
            default :
                break;
        }
    });

    $('#weaver').bind('animationend webkitAnimationEnd MSAnimationEnd oAnimationEnd', function () {
        $('#hearts').attr('class', 'popping');
    });
    var nextStage = function (next) {
        $.scrollTo(0, 100);
        if (4 == next) {
            $('.pyro').show();
        }
        else {
            $('#earth').attr('class', 'step' + next);
        }
        $('#steps').scrollTo('#step' + next, 1000, {axis: 'x'});
            gaTrack(['_trackEvent', 'Magpie Bridge', 'nextStage', next.toString()]);

    };
    $('#login-fb').click(function () {
        if (pageLiked) {
            nextStage(1);
        }
        else {
            FB.login(function (response) {
                if (response && response.authResponse) {
                    var user_id = response.authResponse.userID;
                    var fql_query = "SELECT uid FROM page_fan WHERE page_id = " + page_id + "and uid=" + user_id;
                    FB.Data.query(fql_query).wait(function (rows) {
                        if (rows.length == 1 && rows[0].uid == user_id) {
                            nextStage(1);
                        }
                    });
                }
            }, {scope: 'user_likes'});
        }
    });
    window.fbAsyncInit = function () {
        FB.Event.subscribe('edge.create', function (response) {
            if ('https://facebook.com/MozillaTaiwan' == response) {
                nextStage(1);
            }
        });
        FB.getLoginStatus(function (response) {
            if (response && response.authResponse) {
                var user_id = response.authResponse.userID;
                var fql_query = "SELECT uid FROM page_fan WHERE page_id = " + page_id + "and uid=" + user_id;
                FB.Data.query(fql_query).wait(function (rows) {
                    if (rows.length == 1 && rows[0].uid == user_id) {
                        pageLiked = true;
                    }
                });
            }
        });
    };
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
                var token = $('#subscription').attr('data-csrf-token');
                $.post('/campaign/chinese-valentines-day/participate/', {csrfmiddlewaretoken: token, subscriber: subscriber}, function(response) {
                });
                nextStage(4);
            }
        }
    },false);

    $('#share-post').click(function () {
        FB.ui(
            {
                method: 'feed',
                link: randomPost.attr('href')
            },
            function (response) {
                if (response && response.post_id) {
                    nextStage(2);
                }
            }
        );
    });
    $('#share-video').click(function () {
        FB.ui(
            {
                method: 'feed',
                link: randomVideo.attr('href')
            },
            function (response) {
                if (response && response.post_id) {
                    nextStage(3);
                }
            }
        );
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

    $('#enlarge-notebook').click(function() {
        $('#popup').show();
    });
    $('#popup').click(function(e) {
        if (e.target == this) {
            $('#popup').hide();
        }
    });
})();