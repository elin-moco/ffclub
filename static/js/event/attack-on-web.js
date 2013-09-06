jQuery(document).ready(function() {
	$(window).scroll(function(){
		if ($(window).scrollTop()<=200){
			if($('#masthead').hasClass('fixed')){
				$('#masthead').removeClass('fixed');
				if($('#tabzilla').hasClass('tabzilla-opened'))
					$("html, body").animate({ scrollTop: 0 }, 600);
	    	}
		}else{
			if(!$('#masthead').hasClass('fixed'))
				$('#masthead').addClass('fixed');
		}
		if(!$('#tabzilla').hasClass('tabzilla-opened')){
			if ($(window).scrollTop()!=0)
				if(!$('#masthead').hasClass('fixed'))
					$('#masthead').addClass('fixed');
		}
		return false;
	});
	if ($(window).scrollTop()!=0)
		if(!$('#masthead').hasClass('fixed'))
			$('#masthead').addClass('fixed');
	return false;
});

// scroll action buttom #19105
$('#menu-principal.menu li a').click(function() {
	$('body, html').stop();
	$('body, html').animate({ scrollTop: ($($(this).attr("href")).offset().top - 70) }, "slow");
	return false;
});