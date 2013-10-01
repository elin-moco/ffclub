(function () {
	function remove(id)
	{
    	return (elem=document.getElementById(id)).parentNode.removeChild(elem);
	}
	var film_ids = new Array();
	var n1, n2, tmp, videoContainer;
	film_ids[0] = '//www.youtube.com/embed/QEDvKYUCD38';
	film_ids[1] = '//www.youtube.com/embed/IhqP4Vl-ODk';
	film_ids[2] = '//www.youtube.com/embed/SbSiKqgcg3s';
	film_ids[3] = '//www.youtube.com/embed/oUm9iKAkHlQ';
	for(i=0; i < 4; i++){
		n1 = Math.floor(Math.random() * 4);
		n2 = Math.floor(Math.random() * 4);
		tmp = film_ids[n1];
		film_ids[n1] = film_ids[n2];
		film_ids[n2] = tmp;
	}
	for(i= 0; i < 4; i++){
		videoContainer = document.createElement("P");
		ifrm = document.createElement("IFRAME");
		ifrm.setAttribute("src", film_ids[i]);
		ifrm.style.width = 420+"px";
		ifrm.style.height = 315+"px";
		ifrm.frameborder="0";
		ifrm.style.border="0px none";
		ifrm.allowfullscreen=true;
		videoContainer.appendChild(ifrm);
		document.getElementById("main-context").appendChild(videoContainer);
	}
	//document.getElementById("film-loading").remove();
	remove("film-loading");
})();