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

	$('span.toggle').click(function(e){
		e.preventDefault();
		if ( $(this).attr('data-nav') ==='opened' ){
			$('body').removeClass('opennav');
			$('span.toggle').attr('data-nav', 'closed');
		}else{
			$('body').addClass('opennav');
			$('span.toggle').attr('data-nav', 'opened');
		}
	});

});