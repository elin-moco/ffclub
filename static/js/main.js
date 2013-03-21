"use strict";

$(function(){

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

});