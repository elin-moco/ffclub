"use strict";

(function () {

    var showFireworks = function() {
        var fwElement = '<div class="pyro"><div class="before"></div><div class="after"></div></div>';
        $(fwElement).insertAfter('#heading');
    };

    $('#weaver').bind('animationend webkitAnimationEnd MSAnimationEnd oAnimationEnd', function () {
        $('#hearts').attr('class', 'popping');
        showFireworks();
    });

})();