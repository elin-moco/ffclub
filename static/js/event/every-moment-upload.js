"use strict";


(function () {
//    var maxWidth = 320;
//    var maxHeight = 480;
    var maxWidth = 250;
    var maxHeight = 382;
    var ratio = maxWidth / maxHeight
    var horizontal = true;

    function resizeImage(image, rotated) {
        if (image.width / image.height > ratio) {
            if (rotated) {
                image.height = image.height / image.width * maxHeight;
                image.width = maxHeight;
            }
            else {
                image.width = image.width / image.height * maxHeight;
                image.height = maxHeight;
            }
        }
        else {
            if (rotated) {
                image.width = image.width / image.height * maxWidth;
                image.height = maxWidth;
            }
            else {
                image.height = image.height / image.width * maxWidth;
                image.width = maxWidth;
            }
        }
        if (rotated) {
            $('#dragger').css('width', image.height).css('height', image.width);
        }
        else {
            $('#dragger').css('width', image.width).css('height', image.height);
        }
    }

    function initImagePosition(image, rotated) {
        var width = rotated ? image.height : image.width;
        var height = rotated ? image.width : image.height;
        var container = $('#container');
        if (rotated) {
            var adjustment = (image.width - image.height) / 2;
            $(image).css('left', -adjustment).css('top', adjustment);
        }
        if (width / height > ratio || (width / height <= ratio && rotated)) {
            var initPosition = maxWidth - width;
            $('#dragger').css('left', -initPosition/2);
            container.css('width', (width * 2 - maxWidth) + 'px');
            container.css('height', maxHeight + 'px');
            container.css('left', initPosition + 'px');
            container.css('top', '0');
            horizontal = true;
            $('input#dragLeft').attr('value', -initPosition / 2);
            $('input#dragTop').attr('value', 0);
        }
        else {
            var initPosition = maxHeight - height;
            $('#dragger').css('top', -initPosition/2);
            container.css('height', (height * 2 - maxHeight) + 'px');
            container.css('width', maxWidth + 'px');
            container.css('top', initPosition + 'px');
            container.css('left', '0');
            $('input#dragTop').attr('value', -initPosition / 2);
            $('input#dragLeft').attr('value', 0);
            horizontal = false;
        }
    }

    function loadImage(e) {
        var image = new Image();
        image.onload = function (e) {
            var bin = atob(e.target.src.split(',')[1]);
            var exif = EXIF.readFromBinaryFile(new BinaryFile(bin));
            var rotated = false;
            switch (exif.Orientation) {
                case 8:
                    $(this).removeClass().addClass('rotate-90');
                    rotated = true;
                    break;
                case 3:
                    $(this).removeClass().addClass('rotate180');
                    break;
                case 6:
                    $(this).removeClass().addClass('rotate90');
                    rotated = true;
                    break;
                default:
                    break;
            }
            $('#dragger').draggable({disabled: true});
            $('#dragger').empty();
            $('#container').removeAttr('style');
            $('#dragger').removeAttr('style');
            resizeImage(this, rotated);
            initImagePosition(this, rotated);
            $(image).appendTo('#dragger');
            $('div.entrance').removeAttr('class').addClass('uploaded');
            $('.curtain').hide();
            if (image.width / image.height != ratio) {
                $('#dragger').draggable('enable');
                $('#dragger').draggable({
                    containment: "#container",
                    scroll: false,
                    axis: horizontal ? 'x' : 'y',
                    stop: function() {
                        var left = $(this).css('left').replace('px', '');
                        var top = $(this).css('top').replace('px', '');
                        var width = $(this).css('width').replace('px', '');
                        var height = $(this).css('height').replace('px', '');
                        if (horizontal) {
                            left = width - maxWidth - left;
                            top = 0;
                        }
                        else {
                            top = height - maxHeight - top;
                            left = 0;
                        }
                        $('input#dragLeft').attr('value', left);
                        $('input#dragTop').attr('value', top);
                    }
                });
            }
        };
        image.src = e.target.result;
    }


    function previewImage() {
        var reader = new FileReader();
        var file = document.getElementById("id_image_large").files[0];
        reader.readAsDataURL(file);
        reader.onload = loadImage;
    }

    $('input#frameWidth').attr('value', maxWidth);
    $('input#frameHeight').attr('value', maxHeight);
    $('#id_image_large').change(previewImage);
    $('.choose-file').click(function () {
        $('#id_image_large').click();
    });
    $('.upload-button').click(function() {
        $('form.details-form').submit();
    });
})();