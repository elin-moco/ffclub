"use strict";


(function () {
    $('.vote-control .vote').click(function (e) {
        e.preventDefault();
        var voteUrl = $(this).attr('data-vote-url');
        if (voteUrl) {
            $.ajax({
                dataType: 'json',
                url: voteUrl
            }).done(function (response) {
                    if ('success' == response.result) {
                        var $voteCountElem = $('.voteCount');
                        var voteCount = parseInt($voteCountElem.text()) + 1;
                        $voteCountElem.text(voteCount);
                        alert(response.message)
                    }
                    else {
                        alert(response.errorMessage);
                    }
                }
            );
        }
    });
})();