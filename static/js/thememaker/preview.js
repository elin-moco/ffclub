"use strict";

$(function() {
    install_theme_listener();
});

function install_theme_listener() {
  $('a.install_theme').on('click', function(e){
    var $that = $(this);
    e.preventDefault();
    var div_tag = $that.parent().parent();
    console.log('thememaker preview');
    console.log(div_tag.children('div.demo_section').children('span.demo_font1').attr('color'));
    var theme = {
      id         : div_tag.attr('theme-id'),
      name       : div_tag.children('div#preview_detail').children('h3.meta_title').attr('title'),
      headerURL  : div_tag.children('div.demo_section').children('span.demo_bg').attr('header-img'),
      footerURL  : '/static/uploads/theme_maker/user/00.png',
      textcolor  : div_tag.children('div.demo_section').children('span.demo_font1').attr('color'),
      accentcolor: div_tag.children('div.demo_section').children('span.demo_mask').attr('color'),
    };
    setTheme($that.get(0), theme, INSTALL);
  });
}