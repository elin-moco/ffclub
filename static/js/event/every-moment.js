/**
 * Scratch-off canvas
 *
 * NOTE: this code monkeypatches Function.prototype.bind() if it doesn't
 * already exist.
 *
 * NOTE: This is demo code that has been converted to be less demo-y.
 * But it is still demo-y.
 *
 * To make (more) correct:
 *  o   add error handling on image loads
 *  o   fix inefficiencies
 *
 * depends on jQuery>=1.7
 *
 * Copyright (c) 2012 Brian "Beej Jorgensen" Hall <beej@beej.us>
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

Scratcher = (function () {

    /**
     * Helper function to extract the coordinates from an event, whether the
     * event is a mouse or touch.
     */
    function getEventCoords(ev) {
        var first, coords = {};
        var origEv = ev.originalEvent; // get from jQuery

        if (origEv.changedTouches != undefined) {
            first = origEv.changedTouches[0];
            coords.pageX = first.pageX;
            coords.pageY = first.pageY;
        } else {
            coords.pageX = ev.pageX;
            coords.pageY = ev.pageY;
        }

        return coords;
    }

    /**
     * Helper function to get the local coords of an event in an element.
     *
     * @param elem element in question
     * @param ev the event
     */
    function getLocalCoords(elem, coords) {
        var offset = $(elem).offset();
        return {
            'x': coords.pageX - offset.left,
            'y': coords.pageY - offset.top
        };
    }

    /**
     * Construct a new scratcher object
     *
     * @param canvasId [string] the canvas DOM ID, e.g. 'canvas2'
     * @param backImage [string, optional] URL to background (bottom) image
     * @param frontImage [string, optional] URL to foreground (top) image
     */
    function Scratcher(canvasId, backImage) {
        this.canvas = {
            'main': $('#' + canvasId).get(0)
        };

        this.mouseDown = true;

        this.canvasId = canvasId;

        this._setupCanvases(); // finish setup from constructor now

        this.setImages(backImage);

        this._eventListeners = {};
    }

    /**
     * Set the images to use
     */
    Scratcher.prototype.setImages = function (backImage) {
        this.image = {
            'back': { 'url': backImage, 'img': null }
        };

        if (backImage) {
            this._loadImages(); // start image loading from constructor now
        }
    };

    /**
     * Returns how scratched the scratcher is
     *
     * By adjusting the stride, you get a less accurate result, but it is
     * quicker to compute (pixels are skipped)
     *
     * @param stride [optional] pixel step value, default 1
     *
     * @return the fraction the canvas has been scratched (0.0 -> 1.0)
     */
    Scratcher.prototype.fullAmount = function (stride) {
        var i, l;
        var can = this.canvas.main;
        var ctx = can.getContext('2d');
        var count, total;
        var pixels, pdata;

        if (!stride || stride < 1) {
            stride = 1;
        }

        stride *= 4; // 4 elements per pixel

        pixels = ctx.getImageData(0, 0, can.width, can.height);
        pdata = pixels.data;
        l = pdata.length; // 4 entries per pixel

        total = (l / stride) | 0;

        for (i = count = 0; i < l; i += stride) {
            if (pdata[i] != 0) {
                count++;
            }
        }

        return count / total;
    };

    /**
     * Draw a scratch line
     *
     * Dispatches the 'scratch' event.
     *
     * @param x,y the coordinates
     * @param fresh start a new line if true
     */
    Scratcher.prototype.scratchLine = function (x, y, fresh) {
        var can = this.canvas.main;
        var ctx = can.getContext('2d');
        ctx.globalCompositeOperation = 'destination-out';
        ctx.lineWidth = 30;
        ctx.lineCap = ctx.lineJoin = 'round';
        ctx.strokeStyle = 'rgba(0,0,0,1)'; // can be any opaque color
        if (fresh) {
            ctx.beginPath();
            // this +0.01 hackishly causes Linux Chrome to draw a
            // "zero"-length line (a single point), otherwise it doesn't
            // draw when the mouse is clicked but not moved:
            ctx.moveTo(x + 0.01, y);
        }
        ctx.lineTo(x, y);
        ctx.stroke();

        // call back if we have it
        this.dispatchEvent(this.createEvent('scratch'));
    };

    /**
     * Set up the main canvas and listeners
     */
    Scratcher.prototype._setupCanvases = function () {
        var c = this.canvas.main;
//    var ctx = c.getContext('2d');
//    ctx.fillStyle = '#f00';
//    ctx.fillRect(0,0,140,140);

        // create the temp and draw canvases, and set their dimensions
        // to the same as the main canvas:
//	this.canvas.draw = document.createElement('canvas');

        /**
         * On mouse move, if mouse down, draw a line
         *
         * We do this on the window to smoothly handle mousing outside
         * the canvas
         */
        function mousemove_handler(e) {
            if (!this.mouseDown) {
                return true;
            }
            var local = getLocalCoords(c, getEventCoords(e));

            this.scratchLine(local.x, local.y, false);

            return false;
        }


        $(document).on('mousemove', mousemove_handler.bind(this));
        $(document).on('touchmove', mousemove_handler.bind(this));
    };


    Scratcher.prototype.recompositeCanvases = function () {
        var can = this.canvas.main;
        var ctx = can.getContext('2d');
        ctx.globalCompositeOperation = 'source-over';
        ctx.drawImage(this.image.back.img, 0, 0);
    };
    /**
     * Reset the scratcher
     *
     * Dispatches the 'reset' event.
     *
     */
    Scratcher.prototype.reset = function () {
        // clear the draw canvas
//	this.canvas.draw.width = this.canvas.draw.width;
        this.recompositeCanvases();

        // call back if we have it
        this.dispatchEvent(this.createEvent('reset'));
    };

    /**
     * returns the main canvas jQuery object for this scratcher
     */
    Scratcher.prototype.mainCanvas = function () {
        return this.canvas.main;
    };

    /**
     * Handle loading of needed image resources
     *
     * Dispatches the 'imagesloaded' event
     */
    Scratcher.prototype._loadImages = function () {
        var loadCount = 0;

        // callback for when the images get loaded
        function imageLoaded(e) {
            loadCount++;

            if (loadCount >= 1) {
                this.reset();
                // call the callback with this Scratcher as an argument:
                this.dispatchEvent(this.createEvent('imagesloaded'));
            }
        }

        // load BG and FG images
        for (k in this.image) if (this.image.hasOwnProperty(k)) {
            this.image[k].img = document.createElement('img'); // image is global
            $(this.image[k].img).on('load', imageLoaded.bind(this));
            this.image[k].img.src = this.image[k].url;
        }
    };

    /**
     * Create an event
     *
     * Note: not at all a real DOM event
     */
    Scratcher.prototype.createEvent = function (type) {
        var ev = {
            'type': type,
            'target': this,
            'currentTarget': this
        };

        return ev;
    };

    /**
     * Add an event listener
     */
    Scratcher.prototype.addEventListener = function (type, handler) {
        var el = this._eventListeners;

        type = type.toLowerCase();

        if (!el.hasOwnProperty(type)) {
            el[type] = [];
        }

        if (el[type].indexOf(handler) == -1) {
            el[type].push(handler);
        }
    };

    /**
     * Remove an event listener
     */
    Scratcher.prototype.removeEventListener = function (type, handler) {
        var el = this._eventListeners;
        var i;

        type = type.toLowerCase();

        if (!el.hasOwnProperty(type)) {
            return;
        }

        if (handler) {
            if ((i = el[type].indexOf(handler)) != -1) {
                el[type].splice(i, 1);
            }
        } else {
            el[type] = [];
        }
    };

    /**
     * Dispatch an event
     */
    Scratcher.prototype.dispatchEvent = function (ev) {
        var el = this._eventListeners;
        var i, len;
        var type = ev.type.toLowerCase();

        if (!el.hasOwnProperty(type)) {
            return;
        }

        len = el[type].length;

        for (i = 0; i < len; i++) {
            el[type][i].call(this, ev);
        }
    };

    /**
     * Set up a bind if you don't have one
     *
     * Notably, Mobile Safari and the Android web browser are missing it.
     * IE8 doesn't have it, but <canvas> doesn't work there, anyway.
     *
     * From MDN:
     *
     * https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Function/bind#Compatibility
     */
    if (!Function.prototype.bind) {
        Function.prototype.bind = function (oThis) {
            if (typeof this !== "function") {
                // closest thing possible to the ECMAScript 5 internal
                // IsCallable function
                throw new TypeError("Function.prototype.bind - what is trying to be bound is not callable");
            }

            var aArgs = Array.prototype.slice.call(arguments, 1),
                fToBind = this,
                fNOP = function () {
                },
                fBound = function () {
                    return fToBind.apply(this instanceof fNOP
                        ? this
                        : oThis || window,
                        aArgs.concat(Array.prototype.slice.call(arguments)));
                };

            fNOP.prototype = this.prototype;
            fBound.prototype = new fNOP();

            return fBound;
        };
    }

    return Scratcher;

})();


ImageClock = (function () {

    //Enter path to clock digit images here, in order of 0-9, then colon image:
    ImageClock.digits = ["number-w0.png", "number-w1.png", "number-w2.png", "number-w3.png", "number-w4.png",
        "number-w5.png", "number-w6.png", "number-w7.png", "number-w8.png", "number-w9.png", "dot.png"];
    var root = null;
    var imagePath = '';

    function ImageClock(selector) {
        root = $(selector);
        imagePath = root.attr('data-image-path');
        var preloadImages = [];
        for (var i = 0; i < ImageClock.digits.length; i++) { //preload images
            preloadImages[i] = new Image();
            preloadImages[i].src = imagePath + ImageClock.digits[i];
        }
        setInterval(update, 1000);
    }

    function imageHTML(timeString) {
        var sections = timeString.split(':');
        for (var i = 0; i < sections.length; i++) {
            if (sections[i].length == 1) {
                sections[i] = '<img class="clock-digit" src="' + imagePath + ImageClock.digits[0] + '" />' +
                    '<img class="clock-digit" src="' + imagePath + ImageClock.digits[parseInt(sections[i])] + '" />';
            }
            else {
                sections[i] = '<img class="clock-digit" src="' + imagePath + ImageClock.digits[parseInt(sections[i].charAt(0))] + '" />' +
                    '<img class="clock-digit" src="' + imagePath + ImageClock.digits[parseInt(sections[i].charAt(1))] + '" />';
            }
        }
        return sections[0] + '<img class="clock-colon" src="' + imagePath + ImageClock.digits[10] + '" />' + sections[1] +
            '<img class="clock-colon" src="' + imagePath + ImageClock.digits[10] + '" />' + sections[2];
    }

    function update() {
        var now = new Date();
        var timeString = now.getHours() + ':' + now.getMinutes() + ':' + now.getSeconds();
        var currentTimeHTML = imageHTML(timeString);
        root.empty();
        root.append(currentTimeHTML);
    }

    return ImageClock;

})();

/**
 * This file controls the page logic
 *
 * depends on jQuery>=1.7
 */
(function () {
    var clock;
    var autoScrolling = false;
    /**
     * Returns true if this browser supports canvas
     *
     * From http://diveintohtml5.info/
     */
    function supportsCanvas() {
        return !!document.createElement('canvas').getContext;
    }

    /**
     * Handle scratch event on a scratcher
     */
    function scratcherProgressHandler(ev) {
        // Test every pixel. Very accurate, but might be slow on large
        // canvases on underpowered devices:
        //var pct = (scratcher.fullAmount() * 100)|0;

        // Only test every 32nd pixel. 32x faster, but might lead to
        // inaccuracy:
        var pct = (this.fullAmount(32) * 100) | 0;
        if (pct < 3) {
            var scratcher = $('.scratcher');
            if (!scratcher.hasClass('complete')) {
                scratcher.addClass('complete');
                if (!$('#moment').hasClass('appear')) {
                    $('#moment').addClass('appear')
                }
            }
        }
    }

    function scratcherLoadingHandler(ev) {
        $('.scratcher').show();
    }

    /**
     * Assuming canvas works here, do all initial page setup
     */
    function initScratcher() {
        //	create new scratcher
        var scratcher = new Scratcher('fx-scratcher');

        scratcher.addEventListener('imagesloaded', scratcherLoadingHandler);

        scratcher.setImages('/static/img/event/every-moment/scratch/scratch-gray.png');

        scratcher.addEventListener('scratch', scratcherProgressHandler);
    }

    function initClock() {
        clock = new ImageClock('#clock-content');
        $('#clock').bind('transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd', function () {
            $('#scroll-tip').fadeIn(500);
            $('body').css('overflow-y', 'auto');
        })
    }

    function initAnimations() {
        var controller = $.superscrollorama({playoutAnimations: false});
        var bricksHook = $('#bricks-hook');
        var wonderfulHook = $('#wonderful-experience');
        var builtHook = $('#built-for-you');
        var rulesHook = $('#campaign-rules');
        var timelineHook = $('#campaign-timeline');
        var awardHook = $('#campaign-award');
        var flowHook = $('#campaign-flow');
        var bricks = 'abcedfgh';

        var brickAFall = TweenMax.to($('.phone-brick-a'), 1, {css: {top: 0}});
        var brickBFall = TweenMax.to($('.phone-brick-b'), 1, {css: {top: 0}});
        var brickCFall = TweenMax.to($('.phone-brick-c'), 1, {css: {top: '279px'}});
        var brickDFall = TweenMax.to($('.phone-brick-d'), 1, {css: {top: '279px'}});
        var brickEFall = TweenMax.to($('.phone-brick-e'), 1, {css: {top: '420px'}});
        var brickFFall = TweenMax.to($('.phone-brick-f'), 1, {css: {top: '420px'}});
        var brickGFall = TweenMax.to($('.phone-brick-g'), 1, {css: {top: '420px'}});
        var brickHFall = TweenMax.to($('.phone-brick-h'), 1, {css: {top: '586px'}});

        var brickPage2On = TweenMax.to($('.phone-brick .phone-page2'), 1, {css: {opacity: 1}});
        var brickPage3On = TweenMax.to($('.phone-brick .phone-page3'), 1, {css: {opacity: 1}});
        var foxShow = TweenMax.to($('.phone-brick-wall .fxos-firefox'), 1, {css: {left: '38px'}});
        var brickPage4SlideIn = TweenMax.to($('.phone-brick .phone-page4'), 1, {css: {top: 0}});
        var foxHide = TweenMax.to($('.phone-brick-wall .fxos-firefox'), 1, {css: {top: '100%'}});
        var brickPage4SlideOut = TweenMax.to($('.phone-brick .phone-page4'), 1, {css: {top: '-100%'}});

        function getBrickPage5Slide(brick) {
            return TweenMax.to($('.phone-brick-' + brick + ' .phone-page5'), 1, {css: {left: 0}});
        }

        var brickPage6Slide = TweenMax.to($('.phone-brick .phone-page6'), 1, {css: {left: 0}});

        var brickFallStart = 400;
        var brickFallDur = 400;
        var brickZoomDur = 800;
        var pageSlideDur = 250;
        var brickFallInterval = 200;
        var brickFallPos = brickFallStart;
        var pagePinDur = 1200;

        function resetPos() {
            return brickFallPos = 0;
        }

        function currentPos() {
            return brickFallPos;
        }

        function nextPos() {
            brickFallPos += brickFallInterval;
            return brickFallPos;
        }

        function addNextPos(interval) {
            brickFallPos += interval;
            return brickFallPos;
        }

        var brickWallZoom = TweenMax.to($('.phone-brick-wall'), 1, {css: {'padding': '0 838px 0 0', width: '1920px', height: '1500px'}});
        var brickAZoom = TweenMax.to($('.phone-brick-a'), 1, {css: {top: '0px', left: '0px', width: '828px', height: '558px'}});
        var brickBZoom = TweenMax.to($('.phone-brick-b'), 1, {css: {top: '0px', left: '820px', width: '1110px', height: '860px'}});
        var brickCZoom = TweenMax.to($('.phone-brick-c'), 1, {css: {top: '558px', left: '0px', width: '310px', height: '282px'}});
        var brickDZoom = TweenMax.to($('.phone-brick-d'), 1, {css: {top: '558px', left: '310px', width: '518px', height: '282px'}});
        var brickEZoom = TweenMax.to($('.phone-brick-e'), 1, {css: {top: '836px', left: '0px', width: '950px', height: '660px'}});
        var brickFZoom = TweenMax.to($('.phone-brick-f'), 1, {css: {top: '838px', left: '950px', width: '660px', height: '332px'}});
        var brickGZoom = TweenMax.to($('.phone-brick-g'), 1, {css: {top: '838px', left: '1602px', width: '310px', height: '660px'}});
        var brickHZoom = TweenMax.to($('.phone-brick-h'), 1, {css: {top: '1166px', left: '950px', width: '660px', height: '328px'}});

        var brickBHide1 = TweenMax.to($('.phone-brick-b .phone-page'), 1, {css: {opacity: 0}});
        var brickBHide2 = TweenMax.to($('.phone-brick-b .phone-page6'), 1, {css: {opacity: 0}});
        var woodDeskShow = TweenMax.to($('#rules #description, #wood-desk'), 1, {css: {opacity: 1}});

        var brickWallZoom2 = TweenMax.to($('.phone-brick-wall'), 1, {css: {top: '-90px', 'padding': '0 1257px 0 0', width: '2880px', height: '2250px'}});
        var brickAZoom2 = TweenMax.to($('.phone-brick-a'), 1, {css: {top: '0px', left: '0px', width: '1242px', height: '837px'}});
        var brickBZoom2 = TweenMax.to($('.phone-brick-b'), 1, {css: {top: '0px', left: '1232px', width: '1665px', height: '1290px'}});
        var brickCZoom2 = TweenMax.to($('.phone-brick-c'), 1, {css: {top: '837px', left: '0px', width: '465px', height: '423px'}});
        var brickDZoom2 = TweenMax.to($('.phone-brick-d'), 1, {css: {top: '837px', left: '465px', width: '777px', height: '423px'}});
        var brickEZoom2 = TweenMax.to($('.phone-brick-e'), 1, {css: {top: '1254px', left: '0px', width: '1425px', height: '990px'}});
        var brickFZoom2 = TweenMax.to($('.phone-brick-f'), 1, {css: {top: '1257px', left: '1425px', width: '990px', height: '498px'}});
        var brickGZoom2 = TweenMax.to($('.phone-brick-g'), 1, {css: {top: '1257px', left: '2403px', width: '465px', height: '990px'}});
        var brickHZoom2 = TweenMax.to($('.phone-brick-h'), 1, {css: {top: '1749px', left: '1425px', width: '990px', height: '492px'}});
        var bricksHide = TweenMax.to($('.phone-brick'), 1, {css: {opacity: 0}});

        var woodDeskExpand = TweenMax.to($('#wood-desk'), 1, {css: {width: '120%', top: '-1000px', bottom: '-1000px'}});
        var phoneMove = TweenMax.to($('#rules #description .fxos-phone'), 1, {css: {top: '210px'}});

        var phonePage1Out = TweenMax.to($('#rules #description .fxos-phone .phone-page1'), 1, {css: {left: '-100%', opacity: 0}});
        var phonePage2In = TweenMax.to($('#rules #description .fxos-phone .phone-page2'), 1, {css: {left: 0}});
        var phonePage2Out = TweenMax.to($('#rules #description .fxos-phone .phone-page2'), 1, {css: {left: '-100%', opacity: 0}});
        var phonePage3In = TweenMax.to($('#rules #description .fxos-phone .phone-page3'), 1, {css: {left: 0}});
        var phonePage3Out = TweenMax.to($('#rules #description .fxos-phone .phone-page3'), 1, {css: {left: '-100%', opacity: 0}});
        var phonePage4In = TweenMax.to($('#rules #description .fxos-phone .phone-page4'), 1, {css: {left: 0}});
        var phonePage4Out = TweenMax.to($('#rules #description .fxos-phone .phone-page4'), 1, {css: {left: '-100%', opacity: 0}});

        var woodDeskTurn = TweenMax.to($('#wood-desk'), 1, {css: {transform: 'rotate(90deg)'}});
        var phoneRotate = TweenMax.to($('#rules #description .fxos-phone'), 1, {css: {transform: 'rotate(90deg)', paddingTop: '14px', paddingLeft: '225px', width: '336px', height: '636px', top: '140px'}});

        var nextPhoneFrameIn = TweenMax.to($('#rules #flow .fxos-phone-vertical .phone-frame'), 1, {css: {opacity: 1}});
        var prevPhoneFrameOut = TweenMax.to($('#rules #description .fxos-phone .phone-frame'), 1, {css: {opacity: 0}});
        var phoneBgOut = TweenMax.to($('#rules #description .fxos-phone .phone-bg'), 1, {css: {opacity: 0}});
        var phoneStep1PageIn = TweenMax.to($('#rules #flow .fxos-phone-vertical .phone-page1'), 1, {css: {opacity: 1}});
        var phoneStep1TextIn = TweenMax.to($('#rules #flow .step1'), 1, {css: {opacity: 1}});

        var phoneStep1PageOut = TweenMax.to($('#rules #flow .fxos-phone-vertical .phone-page1'), 1, {css: {left: '-100%', opacity: 1}});
        var phoneStep2PageIn = TweenMax.to($('#rules #flow .fxos-phone-vertical .phone-page2'), 1, {css: {left: '0', opacity: 1}});
        var phoneStep2TextIn = TweenMax.to($('#rules #flow .step2'), 1, {css: {opacity: 1}});

        var phoneStep3FoxIn = TweenMax.to($('#rules #flow .fxos-firefox'), 1, {css: {top: '296px'}});
        var phoneStep3TailIn = TweenMax.to($('#rules #flow .fxos-firefox-tail'), 1, {css: {top: '160px'}});
        var phoneStep3TextIn = TweenMax.to($('#rules #flow .step3'), 1, {css: {opacity: 1}});

        var phoneStep4PageIn = TweenMax.to($('#rules #flow .fxos-phone-vertical .phone-page3'), 1, {css: {left: '0', opacity: 1}});
        var phoneStep4TextIn = TweenMax.to($('#rules #flow .step4'), 1, {css: {opacity: 1}});

        var phoneStep4PageOut = TweenMax.to($('#rules #flow .fxos-phone-vertical .phone-page3'), 1, {css: {left: '-100%', opacity: 1}});
        var phoneStep5PageIn = TweenMax.to($('#rules #flow .fxos-phone-vertical .phone-page4'), 1, {css: {left: '0', opacity: 1}});
        var phoneStep5TextIn = TweenMax.to($('#rules #flow .step5'), 1, {css: {opacity: 1}});

        var phoneStep6StepsUp = TweenMax.to($('#rules #flow .upload-flow'), 1, {css: {top: '120px'}});
        var phoneStep6ButtonIn = TweenMax.to($('.start-upload-button'), 1, {css: {bottom: '180px'}});
        var phoneStep6SpotlightIn = TweenMax.to($('.spotlight'), 1, {css: {bottom: '150px'}});
        var phoneStep6TextIn = TweenMax.to($('.upload-tip'), 1, {css: {bottom: '100px'}});
        var scrollTipOut = TweenMax.to($('#scroll-tip'), 1, {css: {opacity: 0}});

        controller.addTween(bricksHook, brickHFall, brickFallDur, currentPos());
        controller.addTween(bricksHook, brickGFall, brickFallDur, nextPos());
        controller.addTween(bricksHook, brickFFall, brickFallDur, nextPos());
        controller.addTween(bricksHook, brickEFall, brickFallDur, nextPos());
        controller.addTween(bricksHook, brickDFall, brickFallDur, nextPos());
        controller.addTween(bricksHook, brickCFall, brickFallDur, nextPos());
        controller.addTween(bricksHook, brickBFall, brickFallDur, nextPos());
        controller.addTween(bricksHook, brickAFall, brickFallDur, nextPos());

        controller.addTween(bricksHook, brickPage2On, brickFallDur, addNextPos(500));
        controller.addTween(bricksHook, brickPage3On, brickFallDur, addNextPos(1000));
        controller.addTween(bricksHook, foxShow, brickFallDur, addNextPos(500));

        bricksHook.css('height', currentPos() + 'px');
        resetPos();

        controller.addTween(wonderfulHook, brickPage4SlideIn, pageSlideDur, currentPos());
        controller.addTween(wonderfulHook, foxHide, brickFallDur, addNextPos(pagePinDur));
        controller.addTween(wonderfulHook, brickPage4SlideOut, pageSlideDur, currentPos());


        for (var i in bricks) {
            controller.addTween(wonderfulHook, getBrickPage5Slide(bricks[i]), pageSlideDur + (i == 7 ? 250 : 0), addNextPos(pageSlideDur));
        }

        wonderfulHook.css('height', (currentPos() + 250) + 'px');
        resetPos();

        controller.addTween(builtHook, brickPage6Slide, pageSlideDur + 250, addNextPos(1000));

        controller.addTween(builtHook, brickHZoom, brickZoomDur, addNextPos(pageSlideDur + 250));
        controller.addTween(builtHook, brickGZoom, brickZoomDur, currentPos());
        controller.addTween(builtHook, brickFZoom, brickZoomDur, currentPos());
        controller.addTween(builtHook, brickEZoom, brickZoomDur, currentPos());
        controller.addTween(builtHook, brickDZoom, brickZoomDur, currentPos());
        controller.addTween(builtHook, brickCZoom, brickZoomDur, currentPos());
        controller.addTween(builtHook, brickBZoom, brickZoomDur, currentPos());
        controller.addTween(builtHook, brickAZoom, brickZoomDur, currentPos());
        controller.addTween(builtHook, brickWallZoom, brickZoomDur, currentPos());
        controller.addTween(builtHook, brickBHide1, 1, currentPos());
        controller.addTween(builtHook, woodDeskShow, 1, currentPos());
        controller.addTween(builtHook, brickBHide2, 200, addNextPos(brickZoomDur));

        controller.addTween(builtHook, brickHZoom2, brickZoomDur / 2, addNextPos(100));
        controller.addTween(builtHook, brickGZoom2, brickZoomDur / 2, currentPos());
        controller.addTween(builtHook, brickFZoom2, brickZoomDur / 2, currentPos());
        controller.addTween(builtHook, brickEZoom2, brickZoomDur / 2, currentPos());
        controller.addTween(builtHook, brickDZoom2, brickZoomDur / 2, currentPos());
        controller.addTween(builtHook, brickCZoom2, brickZoomDur / 2, currentPos());
        controller.addTween(builtHook, brickBZoom2, brickZoomDur / 2, currentPos());
        controller.addTween(builtHook, brickAZoom2, brickZoomDur / 2, currentPos());
        controller.addTween(builtHook, brickWallZoom2, brickZoomDur / 2, currentPos());
        controller.addTween(builtHook, woodDeskExpand, brickZoomDur / 2, currentPos());
        controller.addTween(builtHook, phoneMove, brickZoomDur / 2, currentPos());

        controller.addTween(builtHook, bricksHide, brickZoomDur / 2, addNextPos(brickZoomDur / 2));

        controller.addTween(builtHook, phonePage1Out, pageSlideDur, currentPos());

        builtHook.css('height', currentPos() + 'px');
        resetPos();

        controller.addTween(rulesHook, phonePage2In, pageSlideDur, currentPos());
        controller.addTween(rulesHook, phonePage2Out, pageSlideDur, addNextPos(pagePinDur));

        rulesHook.css('height', currentPos() + 'px');
        resetPos();

        controller.addTween(timelineHook, phonePage3In, pageSlideDur, currentPos());
        controller.addTween(timelineHook, phonePage3Out, pageSlideDur, addNextPos(pagePinDur));

        timelineHook.css('height', currentPos() + 'px');
        resetPos();

        controller.addTween(awardHook, phonePage4In, pageSlideDur, currentPos());
        controller.addTween(awardHook, phonePage4Out, pageSlideDur, addNextPos(pagePinDur));
        controller.addTween(awardHook, woodDeskTurn, brickZoomDur, addNextPos(pageSlideDur));
        controller.addTween(awardHook, phoneRotate, brickZoomDur, currentPos());

        controller.addTween(awardHook, phoneStep1PageIn, 1, addNextPos(brickZoomDur));
        controller.addTween(awardHook, phoneStep1TextIn, 1, currentPos());

        controller.addTween(awardHook, phoneBgOut, pageSlideDur, currentPos());
        controller.addTween(awardHook, nextPhoneFrameIn, 1, addNextPos(pageSlideDur));
        controller.addTween(awardHook, prevPhoneFrameOut, 1, addNextPos(5));

        controller.addTween(awardHook, phoneStep1PageOut, pageSlideDur, addNextPos(pagePinDur));
        controller.addTween(awardHook, phoneStep2PageIn, pageSlideDur, currentPos());
        controller.addTween(awardHook, phoneStep2TextIn, pageSlideDur, currentPos());
        controller.addTween(awardHook, phoneStep3FoxIn, pageSlideDur, addNextPos(pagePinDur));
        controller.addTween(awardHook, phoneStep3TailIn, pageSlideDur, currentPos());
        controller.addTween(awardHook, phoneStep3TextIn, pageSlideDur, currentPos());
        controller.addTween(awardHook, phoneStep4PageIn, pageSlideDur, addNextPos(pagePinDur));
        controller.addTween(awardHook, phoneStep4TextIn, pageSlideDur, currentPos());
        controller.addTween(awardHook, phoneStep4PageOut, pageSlideDur, addNextPos(pagePinDur));
        controller.addTween(awardHook, phoneStep5PageIn, pageSlideDur, currentPos());
        controller.addTween(awardHook, phoneStep5TextIn, pageSlideDur, currentPos());
        controller.addTween(awardHook, phoneStep6StepsUp, pageSlideDur, addNextPos(600));
        controller.addTween(awardHook, phoneStep6ButtonIn, pageSlideDur, currentPos());
        controller.addTween(awardHook, phoneStep6SpotlightIn, pageSlideDur, currentPos());
        controller.addTween(awardHook, phoneStep6TextIn, pageSlideDur, currentPos());
        controller.addTween(awardHook, scrollTipOut, pageSlideDur, currentPos());

        awardHook.css('height', currentPos() + 'px');

        $('body').keyup(function (e) {
            if (13 == e.keyCode) {
                if (!autoScrolling) {
                    skipScratcher();
                    $.scrollTo($(document).height(), 23000);
                    autoScrolling = true;
                }
                else {
                    $.scrollTo.window().stop(true);
                    autoScrolling = false;
                }
            }
        });
        $.localScroll({
            target: 'body', // could be a selector or a jQuery object too.
            queue: true,
            duration: 1500,
            hash: true,
            onBefore: skipScratcher,
            onAfter: function (anchor, settings) {
                // The 'this' contains the scrolled element (#content)
            }
        });

        $side_nav = $('#side-nav');

        var side_nav_targets = [];
        // store possible nav targets in array for easier searching
        $side_nav.find('a').each(function (index, anchor) {
            side_nav_targets.push(anchor.getAttribute('href'));
        });
        $('.nav-anchor').waypoint(function (direction) {
            $side_nav.find('a').removeClass('curr');

            if (direction === 'down') {
                $side_nav.find('a[href="#' + $(this).attr('id') + '"]').addClass('curr');
            } else {
                // find index in nav array of currently scrolled to target
                var cur_target_index = $.inArray('#' + $(this).attr('id'), side_nav_targets);

                // if there's a previous target, update the active navs
                if (cur_target_index > 0) {
                    $side_nav.find('a[href="' + side_nav_targets[cur_target_index - 1] + '"]').addClass('curr');
                }
            }
        });

    }

    function skipScratcher() {
        if (!$('#moment').hasClass('appear')) {
            $('body').css('overflow-y', 'auto');
            $('#moment').addClass('appear')
            $('#scroll-tip').fadeIn(500);
        }
    }

    /**
     * Handle page load
     */
    $(function () {
        if (supportsCanvas()) {
            $(window).scrollTop(0)
            $('#side-nav a.nav, #main-nav a.rules, #main-nav a.flow, #main-nav a.back-top').click(skipScratcher);
            initScratcher();
            initClock();
            initAnimations();
        } else {
            $('#scratcher-box').hide();
            $('#moment').addClass('appear')
            $('#lamebrowser').show();
        }
    });

})();
