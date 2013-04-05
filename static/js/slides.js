window.saw = (function ($) {

    var controlTemplate = '<button class="prev">Previous</button><button class="next"></button>';

    var wrapperTemplate = function () {
        return '<div class="slidewrap">' +
            controlTemplate +
            '</div>';
    };

    function slideTemplate(slide) {
        return '<div class="slide"><div style="background-image:url(' + slide.url + ')"></div>'+
            '<div class="slideTitle">('+(slide.slideNum+1)+'/'+slideData.length+')  '+slide.title+'</div></div>';
    }

    var container_node,
        wrapper,
        chromeBuilt,
        previousSlidesUrl,

        currentSlide = 0,
        slideData = [],
        preventHide = false,
        boundingBox = [0, 0],
        carousel,
        slideMap = {};


    function buildChrome() {
        wrapper = $(wrapperTemplate()).addClass('slidewrap');
        $('body').append(wrapper);
        boundingBox[0] = wrapper.attr('offsetWidth');
        chromeBuilt = true;
    }

    function handleClicks(e) {
        e.preventDefault();
        var targ = $(e.target);
        if (targ.hasClass('next')) {
            if (!goTo(currentSlide + 1)) {
                jumpToStart();
            }
        }
        else if (targ.hasClass('prev')) {
            if (!goTo(currentSlide - 1)) {
                jumpToEnd();
            }
        }
        else if (targ.hasClass('slidewrap') || !preventHide) {
            hide();
        }

    }

    function attachEvents() {
        wrapper.on('click', handleClicks);
        var bd = document.querySelector('html');
        bd.addEventListener('keyup', handleKeyEvents);
    }


    function init_lightbox() {
        var slides = container_node.find('li');
        slides.each(function (i, el) {
            var thisSlide = {}, thisImg = $(el).find('img');

//            thisSlide.url = thisImg.attr('src').replace(/_s|_q/, '_z');
            thisSlide.url = $(el).find('a').attr('href');
            thisSlide.height = thisImg.attr('data-full-height');
            thisSlide.width = thisImg.attr('data-full-width');
            thisSlide.title = thisImg.attr('title');
            thisSlide.link = $(el).find('a').attr('href');

            slideMap[thisSlide.link] = slideData.push(thisSlide) - 1;
            thisSlide.id = slideMap[thisSlide.link];
        });

    }

    function init_slideshow() {
    }

    function init_carousel() {
        carousel = true;
        wrapper = container_node;
        wrapper.append(controlTemplate);
        var slides = container_node.find('li');
        slides.each(function (i, el) {
            var thisSlide = {}, thisImg = $(el);

            var url = thisImg.css('background-image');
            url = url.substring(5, url.length - 2);
            thisSlide.url = url;
            thisSlide.height = thisImg.attr('data-full-height');
            thisSlide.width = thisImg.attr('data-full-width');
            thisSlide.title = thisImg.attr('title');
            thisSlide.link = url;
            thisSlide.node = thisImg;
            slideData.push(thisSlide);

        });
        attachEvents();
        boundingBox = [ window.innerWidth, window.innerHeight - 20 ];

        jumpToStart(slideData.length - 1);
        attachTouchEvents();
    }

    function jumpTo(to, from) {
        if (from == undefined) {
            from = currentSlide;
        }
        if (to > from) {
            for (; from <= to; from++) {
                goTo(from);
            }
        }
        else if (from > to) {
            for (; from >= to; from--) {
                goTo(from);
            }
        }
    }

    function jumpToStart(i) {
        if (i == undefined) {
            i = currentSlide;
        }
        for (; i >= 0; i--) {
            goTo(i);
        }
    }

    function jumpToEnd(i) {
        if (i == undefined) {
            i = currentSlide;
        }
        for (; i < slideData.length; i++) {
            goTo(i);
        }
    }

    function buildSlide(slideNum) {

        var thisSlide, s, img;

        if (!slideData[slideNum] || slideData[slideNum].node) {
            return false;
        }

        var thisSlide = slideData[slideNum];
        thisSlide.slideNum = slideNum;
        var s = $(slideTemplate(thisSlide));

        img = s.children('div');

        checkImageSize(thisSlide, img);

        thisSlide.node = s;
        wrapper.append(s);
        setPosition(s, boundingBox[0]);

        return s;
    }

    function checkImageSize(thisSlide, img) {
        var scaleFactor = 1, w, h;
        //image is too big! scale it!
        if (thisSlide.width > boundingBox[0] || thisSlide.height > boundingBox[1]) {
            scaleFactor = Math.min(boundingBox[0] / thisSlide.width, boundingBox[1] / thisSlide.height)
            w = Math.round(thisSlide.width * scaleFactor);
            h = Math.round(thisSlide.height * scaleFactor);
            img.css('height', h + 'px');
            img.css('width', w + 'px');

        } else {
            img.css('height', thisSlide.height + 'px');
            img.css('width', thisSlide.width + 'px');
        }
    }

    var i = 0;

    var startPos, endPos, lastPos;

    function handleTouchEvents(e) {

        var direction = 0;

        if (e.type == 'touchstart') {
            startPos = e.touches[0].clientX;
            lastPos = startPos;
            direction = 0;
            if (slideData[currentSlide] && slideData[currentSlide].node) {
                cleanTransitions(slideData[currentSlide].node);
            }

            if (slideData[currentSlide + 1] && slideData[currentSlide + 1].node) {
                cleanTransitions(slideData[currentSlide + 1].node);
            }

            if (slideData[currentSlide - 1] && slideData[currentSlide - 1].node) {
                cleanTransitions(slideData[currentSlide - 1].node);
            }

        } else if (e.type == 'touchmove') {
            if (!carousel) {
                e.preventDefault();
            }
            if (lastPos > startPos) {
                direction = -1;
            } else {
                direction = 1;
            }
            if (slideData[currentSlide]) {
                setPosition(slideData[currentSlide].node, e.touches[0].clientX - startPos);
                if (direction !== 0 && slideData[currentSlide + direction]) {
                    if (direction < 0) {
                        setPosition(slideData[currentSlide + direction].node, (e.touches[0].clientX - startPos) - boundingBox[0]);
                    } else if (direction > 0) {

                        setPosition(slideData[currentSlide + direction].node, (e.touches[0].clientX - startPos) + boundingBox[0]);
                    }

                }
            }

            lastPos = e.touches[0].clientX;
        } else if (e.type == 'touchend') {
            if (lastPos - startPos > 50) {
                goTo(currentSlide - 1);
            } else if (lastPos - startPos < -50) {

                goTo(currentSlide + 1);
            } else {

                //snap back!
                addTransitions(slideData[currentSlide].node);
                setPosition(slideData[currentSlide].node, 0);

                if (slideData[currentSlide + 1] && slideData[currentSlide + 1].node) {
                    addTransitions(slideData[currentSlide + 1]);
                    setPosition(slideData[currentSlide + 1].node, boundingBox[0]);
                }

                if (slideData[currentSlide - 1] && slideData[currentSlide - 1].node) {
                    addTransitions(slideData[currentSlide - 1]);
                    setPosition(slideData[currentSlide - 1].node, 0 - boundingBox[0]);
                }

            }


        }

    }

    function handleKeyEvents(e) {
        if (37 == e.keyCode) {
            if (!goTo(currentSlide - 1)) {
                jumpToEnd();
            }
        }
        else if (39 == e.keyCode) {
            if (!goTo(currentSlide + 1)) {
                jumpToStart();
            }
        }
        else if (27 == e.keyCode) {
            hide();
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

        if (ua.indexOf('WebKit') !== -1) {
            return '-webkit-' + str;
        }

        if (ua.indexOf('Opera') !== -1) {
            return '-o-' + str;
        }

        if (ua.indexOf('Gecko') !== -1) {
            return '-moz-' + str;
        }

        return str;
    }

    function setPosition(node, left) {
        // node.css('left', left +'px');
        node.css(prefixify('transform'), "translate3d(" + left + "px, 0, 0)");
    }

    function addTransitions(node) {
        node.css(prefixify('transition'), prefixify('transform') + ' .25s ease-in-out');

        node[0].addEventListener('webkitTransitionEnd', function (e) {
            window.setTimeout(function () {
                $(e.target).css('-webkit-transition', 'none');
            }, 0)
        })
    }

    function cleanTransitions(node) {
        node.css(prefixify('transition'), 'none');

    }

    function goTo(slideNum) {
        var thisSlide;
        //failure
        if (!slideData[slideNum]) {
            return false;
        }

        if (Math.abs(currentSlide - slideNum) !== 1 && slideData[currentSlide] && slideData[currentSlide].node) {
            //current slide not adjacent to new slide!
            setPosition(slideData[currentSlide].node, (slideNum < currentSlide) ? boundingBox[0] : 0 - boundingBox)
        }

        thisSlide = slideData[slideNum];
        buildSlide(slideNum);
        buildSlide(slideNum + 1);
        buildSlide(slideNum - 1);

        if (thisSlide.node) {
            addTransitions(thisSlide.node);
            setPosition(thisSlide.node, 0);
        }

        if (slideData[slideNum - 1] && slideData[slideNum - 1].node) {
            addTransitions(slideData[slideNum - 1 ].node);
            setPosition(slideData[slideNum - 1 ].node, (0 - boundingBox[0]));
        }

        if (slideData[slideNum + 1] && slideData[slideNum + 1].node) {
            addTransitions(slideData[slideNum + 1 ].node);
            setPosition(slideData[slideNum + 1 ].node, boundingBox[0]);
        }


        currentSlide = slideNum;

        return true;
    }

    function showLightbox(startSlide) {
        if (!chromeBuilt) {
            buildChrome();
        }
        attachEvents();
        wrapper.show();
        boundingBox = [ window.innerWidth, window.innerHeight - 20 ];

        goTo(slideMap[startSlide]);
        attachTouchEvents();
    }

    function showPopup() {
        attachEvents();
        wrapper.show();
    }

    function showSlides(slidesUrl) {
        if (previousSlidesUrl != slidesUrl) {
            previousSlidesUrl = slidesUrl;
            chromeBuilt = false;
            currentSlide = 0;
            slideData = [];
            boundingBox = [0, 0];
            slideMap = {};

            $('.slidewrap').remove();

            $.ajax(
                {
                    dataType: 'html',
                    url: slidesUrl
                }
            ).done(
                function (slides) {
                    $(slides).find('li').each(function (i, el) {
                        var thisSlide = {}, thisImg = $(el).find('img');

                        thisSlide.url = $(el).find('a').attr('href');
                        thisSlide.height = thisImg.attr('data-full-height');
                        thisSlide.width = thisImg.attr('data-full-width');
                        thisSlide.title = thisImg.attr('title');
                        thisSlide.link = $(el).find('a').attr('href');

                        slideData.push(thisSlide);
                    });
                    if (!chromeBuilt) {
                        buildChrome();
                    }
                    attachEvents();
                    wrapper.show();
                    boundingBox = [ window.innerWidth, window.innerHeight ];

                    goTo(0);
                    attachTouchEvents();
                }
            );
        }
        else {
            attachEvents();
            wrapper.show();
            boundingBox = [ window.innerWidth, window.innerHeight - 20 ];
            goTo(0);
            attachTouchEvents();
        }
    }

    function startCarousel(interval) {
        if (interval == undefined) {
            interval = 5000;
        }
        setInterval(function () {
            if (!goTo(currentSlide + 1)) {
                jumpToStart();
            }
        }, interval);
    }

    function hide() {
        if (carousel) {
            return;
        }
        wrapper.hide();
        var bd = document.querySelector('html');
        bd.removeEventListener('touchmove', handleTouchEvents);
        bd.removeEventListener('touchstart', handleTouchEvents);
        bd.removeEventListener('touchend', handleTouchEvents);
        wrapper.off('click', handleClicks);
        bd.removeEventListener('keyup', handleKeyEvents);
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

    function Lightbox(selector) {
        container_node = $(selector);
        init_lightbox();

        return {
            show: showLightbox,
            hide: hide
        };

    }

    function Popup(selector) {
        container_node = $(selector);
        wrapper = container_node;
        wrapper.addClass('slidewrap');
        preventHide = true;
        return {
            show: showPopup,
            hide: hide
        };
    }

    return {
        Lightbox: Lightbox,
        Carousel: Carousel,
        Slideshow: Slideshow,
        Popup: Popup
    };
}($));
