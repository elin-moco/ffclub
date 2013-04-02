window.saw = (function($){
	
	var wrapperTemplate = function() {
		return '<div class="slidewrap">'+
			'<div class="controls"><a class="prev" href="#">prev</a> | <a class="next" href="#">next</a></div>'+
			'</div>';
	};
	
	function slideTemplate(slide){
		return '<div class="slide"><div style="background-image:url('+slide.url+')"></div></div>';
	}
    var container_node,
        wrapper,
        chromeBuilt,
        previousSlidesUrl,

        currentSlide = 0,
        slideData =[],

        boundingBox = [0,0],

        slideMap = {};


    function buildChrome(){
        wrapper = $(wrapperTemplate()).addClass('slidewrap');
        $('body').append(wrapper);
        boundingBox[0] = wrapper.attr('offsetWidth');
        chromeBuilt = true;
    }

    function handleClicks(e){
        e.preventDefault();
        var targ = $(e.target);
        if(targ.hasClass('next')) {
            goTo(currentSlide + 1);
        } else if(targ.hasClass('prev')){
            goTo(currentSlide - 1);
        } else {
            hide();
        }

    }

    function attachEvents(){
        wrapper.on('click', handleClicks);
    }


    function init_lightbox(){
        var slides = container_node.find('li');
        slides.each(function(i, el){
            var thisSlide = {}, thisImg = $(el).find('img');

//            thisSlide.url = thisImg.attr('src').replace(/_s|_q/, '_z');
            thisSlide.url = $(el).find('a').attr('href');
            thisSlide.height = thisImg.attr('data-full-height');
            thisSlide.width = thisImg.attr('data-full-width');
            thisSlide.link = $(el).find('a').attr('href');

            slideMap[thisSlide.link] = slideData.push(thisSlide) - 1;
            thisSlide.id = slideMap[thisSlide.link];
        });

    }

    function init_slideshow(){
    }

    function init_carousel(){
        var slides = container_node.find('li');
        slides.each(function(i, el){
            var thisSlide = {}, thisImg = $(el).find('img');

//            thisSlide.url = thisImg.attr('src').replace(/_s|_q/, '_z');
            thisSlide.url = $(el).find('a').attr('href');
            thisSlide.height = thisImg.attr('data-full-height');
            thisSlide.width = thisImg.attr('data-full-width');
            thisSlide.link = $(el).find('a').attr('href');

            slideMap[thisSlide.link] = slideData.push(thisSlide) - 1;
            thisSlide.id = slideMap[thisSlide.link];
        });
    }

    function buildSlide (slideNum) {

        var thisSlide, s, img, scaleFactor = 1, w, h;

        if(!slideData[slideNum] || slideData[slideNum].node){
            return false;
        }

        var thisSlide = slideData[slideNum];
        var s = $(slideTemplate(thisSlide));

        var img = s.children('div');

        //image is too big! scale it!
        if(thisSlide.width > boundingBox[0] || thisSlide.height > boundingBox[1]){

            if(thisSlide.width > thisSlide.height) {
                scaleFactor = boundingBox[0]/thisSlide.width;
            } else {
                scaleFactor = boundingBox[1]/thisSlide.height;
            }

            w = Math.round(thisSlide.width * scaleFactor);
            h = Math.round(thisSlide.height * scaleFactor);
            img.css('height', h + 'px');
            img.css('width', w + 'px');

        }else{
            img.css('height', thisSlide.height + 'px');
            img.css('width', thisSlide.width + 'px');
        }



        thisSlide.node = s;
        wrapper.append(s);
        setPosition(s, boundingBox[0]);

        return s;
    }

    var i =0;

    var startPos, endPos, lastPos;
    function handleTouchEvents(e){

        var direction = 0;

        if(e.type == 'touchstart'){
            startPos = e.touches[0].clientX;
            lastPos = startPos;
            direction = 0;
            if(slideData[currentSlide] && slideData[currentSlide].node){
                cleanTransitions(slideData[currentSlide].node);
            }

            if(slideData[currentSlide + 1] && slideData[currentSlide + 1].node){
                cleanTransitions(slideData[currentSlide + 1].node);
            }

            if(slideData[currentSlide - 1] && slideData[currentSlide -1].node){
                cleanTransitions(slideData[currentSlide -1].node);
            }

        }else if(e.type == 'touchmove'){
            e.preventDefault();
            if(lastPos > startPos){
                direction = -1;
            }else{
                direction = 1;
            }
            if(slideData[currentSlide]){
                setPosition(slideData[currentSlide].node, e.touches[0].clientX - startPos);
                if(direction !== 0 && slideData[currentSlide + direction]){
                    if(direction < 0){
                        setPosition(slideData[currentSlide + direction].node, (e.touches[0].clientX - startPos) - boundingBox[0]);
                    }else if(direction > 0){

                        setPosition(slideData[currentSlide + direction].node, (e.touches[0].clientX - startPos) + boundingBox[0]);
                    }

                }
            }

            lastPos = e.touches[0].clientX;
        }else if(e.type == 'touchend'){
            if(lastPos - startPos > 50){
                goTo(currentSlide-1);
            } else if(lastPos - startPos < -50){

                goTo(currentSlide+1);
            }else{

                //snap back!
                addTransitions(slideData[currentSlide].node);
                setPosition(slideData[currentSlide].node, 0);

                if(slideData[currentSlide + 1] && slideData[currentSlide + 1].node){
                    addTransitions(slideData[currentSlide + 1]);
                    setPosition(slideData[currentSlide + 1].node, boundingBox[0]);
                }

                if(slideData[currentSlide - 1] && slideData[currentSlide - 1].node){
                    addTransitions(slideData[currentSlide - 1]);
                    setPosition(slideData[currentSlide - 1].node, 0 - boundingBox[0]);
                }

            }


        }

    }

    function attachTouchEvents() {

        var bd = document.querySelector('html');
        bd.addEventListener('touchmove', handleTouchEvents);
        bd.addEventListener('touchstart', handleTouchEvents);
        bd.addEventListener('touchend', handleTouchEvents);

    }

    function prefixify(str) {

        var ua = window.navigator.userAgent;

        if(ua.indexOf('WebKit') !== -1) {
            return '-webkit-' + str;
        }

        if(ua.indexOf('Opera') !== -1) {
            return '-o-' + str;
        }

        if(ua.indexOf('Gecko') !== -1) {
            return '-moz-' + str;
        }

        return str;
    }

    function setPosition(node, left) {
        // node.css('left', left +'px');
        node.css(prefixify('transform'), "translate3d("+left+"px, 0, 0)");
    }

    function addTransitions(node){
        node.css(prefixify('transition'), prefixify('transform') + ' .25s ease-in-out');

        node[0].addEventListener('webkitTransitionEnd', function(e){
            window.setTimeout(function(){
                $(e.target).css('-webkit-transition', 'none');
            }, 0)
        })
    }

    function cleanTransitions(node){
        node.css(prefixify('transition'), 'none');

    }

    function goTo(slideNum){
        var thisSlide;
        //failure
        console.info('GOTO: '+slideData);
        if(!slideData[slideNum]){
            goTo(currentSlide);
            return;
        }

        if(Math.abs(currentSlide - slideNum) !== 1 && slideData[currentSlide] && slideData[currentSlide].node){
            //current slide not adjacent to new slide!
            setPosition(slideData[currentSlide].node, (slideNum < currentSlide)  ? boundingBox[0] : 0 -  boundingBox)
        }

        thisSlide = slideData[slideNum];
        buildSlide(slideNum);
        buildSlide(slideNum + 1);
        buildSlide(slideNum - 1);

        if(thisSlide.node){
            addTransitions(thisSlide.node);
            setPosition(thisSlide.node, 0);
        }

        if(slideData[slideNum - 1] && slideData[slideNum-1].node){
            addTransitions(slideData[slideNum - 1 ].node);
            setPosition( slideData[slideNum - 1 ].node , (0 - boundingBox[0]) );
        }

        if(slideData[slideNum + 1] && slideData[slideNum + 1].node){
            addTransitions(slideData[slideNum + 1 ].node);
            setPosition(slideData[slideNum + 1 ].node, boundingBox[0] );
        }


        currentSlide = slideNum;
    }

    function showLightbox(startSlide){
        if(!chromeBuilt){
            buildChrome();
            attachEvents();
        }
        wrapper.show();
        boundingBox = [ window.innerWidth, window.innerHeight ];

        goTo(slideMap[startSlide]);
        attachTouchEvents();
    }

    function showSlides(slidesUrl){
        if (previousSlidesUrl != slidesUrl) {
            previousSlidesUrl = slidesUrl;
            chromeBuilt = false;
            currentSlide = 0;
            slideData =[];
            boundingBox = [0,0];
            slideMap = {};

            $('.slidewrap').remove();

            $.ajax(
                {
                    dataType: 'html',
                    url: slidesUrl
                }
            ).done(
                function(slides) {
                    $(slides).find('li').each(function(i, el){
                        var thisSlide = {}, thisImg = $(el).find('img');

                        thisSlide.url = $(el).find('a').attr('href');
                        thisSlide.height = thisImg.attr('data-full-height');
                        thisSlide.width = thisImg.attr('data-full-width');
                        thisSlide.link = $(el).find('a').attr('href');

                        slideData.push(thisSlide);

                        console.info(slideData);
                    });
                    if(!chromeBuilt){
                        buildChrome();
                        attachEvents();
                    }
                    wrapper.show();
                    boundingBox = [ window.innerWidth, window.innerHeight ];

                    goTo(0);
                    attachTouchEvents();
                }
            );
        }
        else {
            wrapper.show();
            goTo(0);
            attachTouchEvents();
        }
    }

    function startCarousel() {

    }

    function hide(){
        wrapper.hide();
        var bd = document.querySelector('html');
        bd.removeEventListener('touchmove', handleTouchEvents);
        bd.removeEventListener('touchstart', handleTouchEvents);
        bd.removeEventListener('touchend', handleTouchEvents);
    }

    function Carousel(selector) {
        container_node = $(selector);
        init_carousel();
        return {
            start: startCarousel
        };
    }

    function Slideshow() {
        init_slideshow();

        return {
            show: showSlides,
            hide: hide
        };
    }

    function Lightbox (selector) {
        container_node = $(selector);
		init_lightbox();
		
		return {
			show: showLightbox,
			hide: hide
		};
		
	}
	
	return {
		Lightbox:Lightbox,
        Carousel:Carousel,
        Slideshow:Slideshow
	};
}($));
