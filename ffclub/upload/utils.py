from cStringIO import StringIO
import os
import commonware.log

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


log = commonware.log.getLogger('ffclub')

RESIZE_MODE_ASPECT_FILL = 0
RESIZE_MODE_ASPECT_FIT = 1
RESIZE_MODE_WIDTH_FIT = 2
RESIZE_MODE_HEIGHT_FIT = 3

LARGE_SIZE = (1024, 768)
MEDIUM_SIZE = (320, 480)
SMALL_SIZE = (120, 120)


def compute_crop_box(aspectRatio, original, frame, frameOffset):
    (width, height) = original
    (frameWidth, frameHeight) = frame
    (frameLeft, frameTop) = frameOffset

    if float(width) / float(height) > aspectRatio:
        log.error('Horizontal')
        newWidth = int(round(aspectRatio * height))
        newHeight = height
    else:
        log.error('Vertical')
        newWidth = width
        newHeight = int(round(aspectRatio * width))

    left = frameLeft * newHeight / frameHeight
    top = frameTop * newHeight / frameHeight
    return left, top, newWidth + left, newHeight + top


def compute_new_size(original, limits, resize_mode):
    ratio = 1.0
    (width, height) = original
    (limit_width, limit_height) = (float(limits[0]), float(limits[1]))
    log.debug('Old size: (%d, %d)' % (width, height))
    if resize_mode == RESIZE_MODE_ASPECT_FILL:
        if width > limit_width or height > limit_height:
            ratio = min(limit_width / width, limit_height / height)
    elif resize_mode == RESIZE_MODE_ASPECT_FIT:
        if width > limit_width and height > limit_height:
            ratio = max(limit_width / width, limit_height / height)
    elif resize_mode == RESIZE_MODE_WIDTH_FIT:
        if width > limit_width:
            ratio = limit_width / width
    elif resize_mode == RESIZE_MODE_HEIGHT_FIT:
        if height > limit_height:
            ratio = limit_height / height
    log.debug('New size: (%d, %d)' % (int(round(width * ratio)), int(round(height * ratio))))
    return int(round(width * ratio)), int(round(height * ratio))


def open_image(original_image):
    return Image.open(StringIO(original_image.read()))


def resize_image(name, image, new_size, content_type, rotate_degree=0, crop_box=None):
    suffix = content_type.split('/')[-1]
    if rotate_degree != 0:
        log.debug('Rotate %d' % rotate_degree)
        image = image.rotate(rotate_degree)
    if crop_box:
        log.debug('Crop box: (%d, %d, %d, %d)' % crop_box)
        image = image.resize(new_size, Image.ANTIALIAS)
        image = image.crop(crop_box)
    else:
        image.thumbnail(new_size, Image.ANTIALIAS)
    temp_handle = StringIO()
    image.save(temp_handle, suffix)
    temp_handle.seek(0)
    return SimpleUploadedFile(os.path.split(name)[-1],
                              temp_handle.read(), content_type=content_type)
