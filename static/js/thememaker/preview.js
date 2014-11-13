"use strict";

$(function() {
  init_check();
  install_theme_listener();
  share_theme_listener();
});

function init_check() {
  var logined = document.getElementsByClassName('logined_account');
  //var logined = document.getElementsByClassName('login_account');
  if(logined.length == 0) {
    var loginPopup = new Modal().Popup('.loginPopup');
    var loginHandler = function (e, msg) {
      var title = '登入 Firefox 俱樂部';
      if ($(this).attr('title')) {
        title = $(this).attr('title');
      }
      if (msg) {
        title = msg;
      }
      loginPopup.show(title);
      var fbpile = $('div.fbpile');
      if (fbpile.children().length == 0) {
        fbpile.append('<div class="fb-facepile" data-app-id="' + fbpile.attr('data-app-id') +
          '" data-action="Comma separated list of action of action types" data-width="400" data-max-rows="1"></div>');
        FB.XFBML.parse(fbpile.get(0));
      }
    };
    $('a.upload').addClass('loginButton');
    $('a.upload').click(loginHandler);
  }
}

function install_theme_listener() {
  $('a.install_theme').on('click', function(e){
    var $that = $(this);
    e.preventDefault();
    var div_tag = $that.parent().parent();
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

function share_theme_listener() {
  $('a.upload').on('click', function(e){
    console.log('click share');
    e.preventDefault();
    if (!$('a.upload').hasClass('loginButton')) {
      $('div#share_section').hide();
      $('div#share_cc').show();
    }
  });
  $('a.select_share_cc').on('click', function(e){
    console.log('click cc');
    e.preventDefault();
    $('div#share_cc').hide();
    $('div#upload_section').show();
  });
}