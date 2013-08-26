// scroll action buttom
$("#menu-principal.menu li a").click(function() {
	$('body, html').stop();
	//$('body, html').animate({ scrollTop: ($($(this).attr("href")).offset().top  }, "slow");
	$('body, html').animate({ scrollTop: ($($(this).attr("href")).offset().top ) }, "slow");
	return false;
});