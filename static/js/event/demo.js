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
    var total_width = 0;
    $('#image-gallery img').each(function(index){
        total_width += parseInt(this.width);
    });
    if(total_width >= 900){
        $(".image-panel-button").show();
        $("#image-moving-right").bind( "click", function() {
            $('#image-gallery').animate(
                { 'left': '-=100px' },
                '50',
                'swing',
                function() {
                    if( parseInt($('#image-gallery').css('left')) < -1*(total_width-960)){
                    $('#image-gallery').animate(
                        { 'left':  -1*(total_width-960)+'px'},
                        '50',
                        'swing')
                    return;
                }
            });
        });
        $("#image-moving-left").bind( "click", function() {
            $('#image-gallery').animate(
                { 'left': '+=100px' },
                '50',
                'swing',
                function() {
                    if( parseInt($('#image-gallery').css('left')) > 0){
                    $('#image-gallery').animate(
                        { 'left':  0},
                        '50',
                        'swing')
                    return;
                }
            });
        });
    }
})();