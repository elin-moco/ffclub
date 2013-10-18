"use strict";

$(function(){
    var loginPopup = new Modal().Popup('.loginPopup');
    var loginHandler = function (e, msg) {
        var title = '登入 Firefox 活力軍';
        if ($(this).attr('title')) {
            title = $(this).attr('title');
        }
        if (msg) {
            title = msg;
        }
        loginPopup.show(title);
        var fbpile = $('div.fbpile');
        if (fbpile.children().length == 0) {
            fbpile.append('<div class="fb-facepile" data-app-id="' + fbpile.attr('data-app-id') +
                '" data-action="Comma separated list of action of action types" data-width="400" data-max-rows="1"></div>');
            FB.XFBML.parse(fbpile.get(0));
        }
    };
    $('.loginButton, .loginLink').click(loginHandler);
    $(document).on('ffclubLogin', loginHandler);
/*
	$('#tabzilla').click( function(e){
		e.preventDefault();
		if ( $(this).attr('aria-expanded') == 'true'){
			$('#tabzilla-panel').addClass('close-nav');
			$(this).attr('aria-expanded', 'false').attr('title', '關閉');
		}else{
			$('#tabzilla-panel').removeClass('close-nav');
			$(this).attr('aria-expanded', 'true').attr('title', '打開');
		}
		
	});

	$('span.toggle').click(function(e){
		e.preventDefault();
		if ( $(this).attr('data-nav') ==='opened' ){
			$('#body_wrapper').removeClass('opennav');
			//$('#tabzilla-panel').removeClass('open');
			//$('#outer-wrapper').removeClass('open');
			$('span.toggle').attr('data-nav', 'closed');
		}else{
			$('#body_wrapper').addClass('opennav');
			//$('#tabzilla-panel').addClass('open');
			//$('#outer-wrapper').addClass('open');
			$('span.toggle').attr('data-nav', 'opened');
		}
	});
*/
});