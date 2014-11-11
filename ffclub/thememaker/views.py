import Image
import ImageDraw
from StringIO import StringIO
from django.shortcuts import render, redirect
import re
from ffclub.thememaker.models import ThemeTemplate, UserTheme
from ffclub.settings import THEMES_PER_PAGE, TEMPLATE_THEME_FILE_PATH, USER_THEME_FILE_PATH


def index(request):
    return new(request, 0)


def new(request, page_number):
    return show_themes(request, page_number, 'create_time')


def hot(request, page_number):
    return show_themes(request, page_number, 'download')


def fav(request, page_number):
    return show_themes(request, page_number, 'likes')


def show_themes(request, page_number, theme_type):

    page = 1
    if page_number != '':
        page = int(page_number)
    if page < 1:
        page = 1

    offset = ((page - 1) * THEMES_PER_PAGE)
    limit = offset + THEMES_PER_PAGE
    cover_themes = UserTheme.objects.filter(covered=1)[0:5]
    user_themes = UserTheme.objects.order_by('-' + theme_type)[offset:limit]

    if len(user_themes) == 0:
        theme_block = 'theme_none'
    else:
        theme_block = 'theme_block'

    url_mapping = {
        'create_time': 'new',
        'download': 'hot',
        'likes': 'fav'
    }

    color_mapping = {
        '#FFF': 'Whitecolor',
        '#FD3C60': 'Redcolor',
        '#FADC49': 'Yellowcolor',
        '#33F340': 'Greencolor',
        '#88E8FC': 'Bluecolor',
    }

    class_mapping = {
        'create_time': 'theme_latest',
        'download': 'theme_hot',
        'likes': 'theme_favorite'
    }

    menu_mapping = {
        'theme_latest': 'on' if theme_type == 'create_time' else '',
        'theme_hot': 'on' if theme_type == 'download' else '',
        'theme_favorite': 'on' if theme_type == 'likes' else '',
    }

    display_mapping = {
        'theme_latest': '' if theme_type == 'create_time' else 'display:none',
        'theme_hot': '' if theme_type == 'download' else 'display:none',
        'theme_favorite': '' if theme_type == 'likes' else 'display:none',
    }

    data = {
        'theme_block': theme_block,
        'theme_type': theme_type,
        'theme_class': class_mapping,
        'url_mapping': url_mapping,
        'menu_mapping': menu_mapping,
        'display_mapping': display_mapping,
        'color_mapping': color_mapping,
        'cover_themes': cover_themes,
        'user_themes': user_themes,
    }

    return render(request, 'thememaker/index.html', data)


def create(request):
    template_themes = ThemeTemplate.objects.filter(enabled=1)[0:30]

    data = {
        'template_themes': template_themes,
    }
    return render(request, 'thememaker/create.html', data)


def submit(request):

    if request.method == 'POST':
        template_id = request.POST.get('template_id')
        user_title = request.POST.get('title')
        user_description = request.POST.get('description')
        user_image = request.POST.get('user_image')

    data_url_pattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
    user_image = data_url_pattern.match(user_image).group(2)
    user_image = Image.open(StringIO(user_image.decode('base64')))

    theme_template = ThemeTemplate.objects.get(id=template_id)
    color_bundle = theme_template.color
    template_image = Image.open(theme_template.template_image.name)
    edit_image = Image.open(theme_template.edit_image.name)

    user_theme = UserTheme(title=user_title, description=user_description,
                           header_image='000.png',
                           icon_image=theme_template.icon_image,
                           preview_image='000.png',
                           bg_color=color_bundle.bg_color, font_color=color_bundle.font_color,
                           template=theme_template, category=theme_template.category)
    user_theme.save()
    print user_theme.id

    user_image = user_image.crop((45, 60, 1000, 300))

    header_image = Image.new('RGBA', (3000, 200))
    header_image.paste(user_image, (2094, 0), user_image)
    header_image.paste(template_image, (0, 0), template_image)
    header_image_path = USER_THEME_FILE_PATH + str(user_theme.id) + ".png"
    header_image.save(header_image_path)

    preview_image = Image.new('RGBA', (928, 200))
    preview_image.paste(user_image, (22, 0), user_image)
    preview_image.paste(edit_image, (0, 0), edit_image)
    preview_image_path = USER_THEME_FILE_PATH + str(user_theme.id) + "-cut.png"
    preview_image.save(preview_image_path)

    user_theme.header_image = header_image_path
    user_theme.preview_image = preview_image_path
    user_theme.save()
    request.session['theme_id'] = user_theme.id

    return redirect(preview)


def preview(request):

    theme_id = request.session.get('theme_id', 35)
    print theme_id

    user_theme = UserTheme.objects.get(id=int(theme_id))
    data = {
        'user_theme': user_theme,
    }
    return render(request, 'thememaker/preview.html', data)


def theme(request, theme_id):
    user_theme = UserTheme.objects.get(id=theme_id)
    data = {
        'user_theme': user_theme,
    }
    return render(request, 'thememaker/preview.html', data)


def publish(request, theme_id):
    """ AJAX method to publish user theme """
    user_theme = UserTheme.objects.get(id=theme_id)
    user_theme.enabled = 1
    user_theme.save()
    return "OK"


def inc_views(request, theme_id):
    """ AJAX method to increase the views of specific user theme """
    return "OK"


def inc_downloads(request, theme_id):
    """ AJAX method to increase the downloads of specific user theme """
    return "OK"


def update_likes(request, theme_id, likes):
    """ AJAX method to update the likes of specific user theme """
    return "OK"