"use strict";

$(function() {
  init();
  build_theme_url();
  login_check();

  if (!is_firefox_browser()) {
    replace_with_firefox_download();
  } else {
    install_theme_listener();
  }
  
  share_theme_listener();
  create_qrcode();
});

function is_firefox_browser() {
  if (navigator.userAgent.search("Firefox") > -1) {
    return true;
  }
  return false;
}

function replace_with_firefox_download() {
  var message = '下載 Firefox';
  $('a.install_theme').attr('title', message);
  $('a.install_theme').text(message);
  $('a.install_theme').on('click', function(e){
    e.stopPropagation();
  });
}

function init() {
  var cc_type = $('select#cc_option').attr('cctype');
  $('div#preview_detail > ul > li:nth-child(' + parseInt(cc_type) + ')').show();

  var path = window.location.pathname;
  if (path.indexOf("preview") < 0) {
    $('div#share_section').hide();
    $('div#share_cc').hide();
    $('div#upload_section').show();
    $('div#qrcode').show();
  }
}

function build_theme_url() {
  $('div#address_section > a').text(get_theme_url());
  $('div#address_section > a').attr('href', get_theme_url());
  $('li.share_fb > a').attr('href', 'https://www.facebook.com/sharer/sharer.php?u=' + get_theme_url());
  $('li.share_google > a').attr('href', 'http://plus.google.com/share?url=' + get_theme_url());
  $('li.share_twitter > a').attr('href', 'http://twitter.com/share?text=我的Firefox自製佈景主題&url=' + get_theme_url());
  $('li.share_pinterest > a').attr('href', 'http://pinterest.com/pin/create/button/?media=' + get_theme_url());
}

function login_check() {
  var logined = document.getElementsByClassName('logined_account');
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
    $.post('/thememaker/inc_downloads', {theme_id: div_tag.attr('theme-id'), }, function (response) {});
  });
}

function share_theme_listener() {
  $('a.upload').on('click', function(e){
    console.log('click share');
    e.preventDefault();
    if (!$('a.upload').hasClass('loginButton')) {
      $.post('/thememaker/publish', {theme_id: $('div#preview_section').attr('theme-id')}, function (response) {});
      $('div#share_section').hide();
      $('div#share_cc').show();
    }
  });
  $('a.select_share_cc').on('click', function(e){
    console.log('click cc');
    e.preventDefault();
    var cc_option = $( "#cc_option option:selected" ).val();;
    $.post('/thememaker/cc_option', {theme_id: $('div#preview_section').attr('theme-id'), option: cc_option}, function (response) {});
    $('div#share_cc').hide();
    $('div#upload_section').show();
    $('div#qrcode').show();
    history.pushState({}, null, '/thememaker/theme/' + $('#preview_section').attr('theme-id'));
  });
}

function create_qrcode() {
  new QRCode(document.getElementById("qrcode"), get_theme_url());
}

function get_theme_url() {
  return "http://" + window.location.hostname + "/thememaker/theme/" + $('#preview_section').attr('theme-id');  
}