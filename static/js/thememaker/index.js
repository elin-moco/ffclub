"use strict";

$(function() {
  scroll_to_tab_listener();
  infinitescroll_listener();
  slider_listener();
  expand_theme_listener();

  if (!is_firefox_browser()) {
    replace_with_firefox_download();
  } else {
    install_cover_theme_listener();
    install_theme_listener();
  }
});

function is_firefox_browser() {
  if (navigator.userAgent.search("Firefox") > -1) {
    return true;
  }
  return false;
}

function replace_with_firefox_download() {
  var message = '下載 Firefox 以安裝佈景';
  $('a.install').attr('title', message);
  $('a.install').text(message);
  $('a.install').on('click', function(e){
    e.stopPropagation();
  });
}

function scroll_to_tab_listener() {
  var path = window.location.pathname;
  var isScroll = false;
  isScroll = (path.indexOf("new") > -1)? true : isScroll;
  isScroll = (path.indexOf("fav") > -1)? true : isScroll;
  isScroll = (path.indexOf("hot") > -1)? true : isScroll;

  if (isScroll) {
    $('html, body').animate({
      scrollTop: $("#theme_list").offset().top
    }, 1000);
  }

}

function infinitescroll_listener() {
  $('#theme_wrap').infinitescroll({
    navSelector: '#page-nav',
    nextSelector: '#page-nav > a',
    itemSelector: 'li.theme_block',
    loadingImg: '',
    loadingText: '',
    donetext: '',
    animate: true,
    loading: {
      finished: undefined,
      finishedMsg: "",
      img: "",
      msg: null,
      msgText: "",
      selector: null,
      speed: 'fast',
      start: undefined
    },
  }, function() {
    expand_theme_listener();
    if (!is_firefox_browser()) {
      replace_with_firefox_download();
    } else {
      install_cover_theme_listener();
      install_theme_listener();
    }
  });
}

function install_cover_theme_listener() {
  $('#cover_theme a.install').on('click', function(e){
    e.preventDefault();
    e.stopPropagation();
    var $that = $(this);
    var li_tag = $that.parent().parent();
    var theme = {
      id         : li_tag.attr('theme-id'),
      name       : li_tag.children('h3.meta_title').attr('title'),
      headerURL  : li_tag.children('div.demo_section').children('span.demo_bg').attr('header-img'),
      footerURL  : '/static/uploads/theme_maker/user/00.png',
      textcolor  : li_tag.children('div.demo_section').children('span.demo_font1').attr('color'),
      accentcolor: li_tag.children('div.demo_section').children('span.demo_mask').attr('color'),
    };
    setTheme($that.get(0), theme, INSTALL);
    $.post('/thememaker/inc_downloads', {theme_id: li_tag.attr('theme-id'), }, function (response) {});
  });
}

function install_theme_listener() {
  $('div.theme_bottom_btn > a.install').unbind();
  $('div.theme_bottom_btn > a.install').on('click', function(e){
    var $that = $(this);
    e.preventDefault();
    e.stopPropagation();
    var li_tag = $that.parent().parent();
    var theme = {
      id         : li_tag.attr('theme-id'),
      name       : li_tag.children('h3.meta_title').attr('title'),
      headerURL  : li_tag.children('dl').children('dt').children('img').attr('header-img'),
      footerURL  : '/static/uploads/theme_maker/user/00.png',
      textcolor  : li_tag.children('dl').children('dd.theme_text').attr('color'),
      accentcolor: li_tag.children('dl').children('dd.theme_mask').attr('color'),
    };
    setTheme($that.get(0), theme, INSTALL);
    $.post('/thememaker/inc_downloads', {theme_id: li_tag.attr('theme-id'), }, function (response) {
      var download_times = li_tag.children('p.tab_type').children('span.type_hot').text().split(" ");
      var new_download_times = (parseInt(download_times[0]) + 1).toString() + " " + download_times[1];
      li_tag.children('p.tab_type').children('span.type_hot').text(new_download_times);
    });
  });
}

function expand_theme_listener() {
  $('div.theme_container > ul > li').unbind();
  $('div.theme_container > ul > li').on('click', function(e){
    e.preventDefault();
    e.stopPropagation();
    var $that = $(this);
    var expand = $that.children('div.theme_bottom_btn').children('a.expand');
    var isOpen = expand.hasClass('on');
    var li_tag = $that;
    var ul_tag = $that.parent();
    var li_idx = $(ul_tag).children('li').index(li_tag) + 1;
    var div_tag = $that.parent().parent();

    $('div.theme_bottom_btn > a.expand').removeClass('on');
    $('#theme_detail').slideUp(400, function(){
      $('#expand_arrow').removeClass('arrow01 arrow02 arrow03').addClass('arrow0' + li_idx);  
      $(div_tag).after($('#theme_detail'));
      loadSocialButtons(li_tag.attr('theme-id'));
      fill_data(li_tag);
      build_theme_url(li_tag.attr('theme-id'));
    });
    if (!isOpen) {
      expand.addClass('on');
      $('#theme_detail').slideDown(400);
      $.post('/thememaker/inc_views', {theme_id: li_tag.attr('theme-id'), }, function (response) {});
    }   
  });

  $('a.btn_close').unbind();
  $('a.btn_close').on('click', function(e){
    e.preventDefault();
    $('#theme_detail').slideUp(400);
    $('div.theme_bottom_btn > a.expand').removeClass('on');
  });

  function loadSocialButtons(id) {
    if (FB && gapi) {
      var url = get_theme_url(id);
      var fb = $('li.facebookLike');
      var gp = $('li.googlePlus');
      if (fb.children().length == 0) {
        fb.append('<div class="fb-like" data-send="false"' +
          'data-href="' + url + '"' +
          'data-layout="button_count" data-width="150" data-show-faces="false"></div>');
        FB.XFBML.parse(fb.get(0));
      }
      if (gp.children().length == 0) {
        gp.append('<div class="g-plusone" data-size="medium" data-href="' + url + '"></div>');
        gapi.plusone.go(gp.get(0));
      }
    }
  };

  // fill data into #theme_detail element
  function fill_data(ele) {
    var p_tag = ele.children('p.tab_type');
    var meta_title = ele.children('h3').text();
    var meta_desc = ele.children('p.meta_desc').text();
    var meta_date = p_tag.children('span.type_latest').text();
    var meta_download = p_tag.children('span.type_hot').text();
    var meta_likes = p_tag.children('span.type_favorite').text();
    var preview_img = ele.children('dl').children('dt').children('img').attr('src');
    var color = ele.children('dl').children('dd.theme_mask').attr('color');

    $('#theme_detail_panel h3').text(meta_title);
    $('#theme_detail_panel p').text(meta_desc);
    $('#theme_detail_panel ul li.info_date').text(meta_date);
    $('#theme_detail_panel ul li.info_download').text(meta_download);
    $('#theme_detail_panel ul li.info_fb').text(meta_likes);
    $('#theme_detail_panel div.demo_section span.demo_bg').css("background-image", "url('" + preview_img + "')");
    $('#theme_detail_panel div.demo_section span.demo_bg').css("background-position", "right top");
    $('div#theme_detail').removeClass('Whitecolor Redcolor Yellowcolor Greencolor Bluecolor');
    $('div#theme_detail').addClass(color);
  }

  function build_theme_url(id) {
    $('div#address_section > a').text(get_theme_url(id));
    $('div#address_section > a').attr('href', get_theme_url(id));
    $('li.share_fb > a').attr('href', 'https://www.facebook.com/sharer/sharer.php?u=' + get_theme_url(id));
    $('li.share_google > a').attr('href', 'http://plus.google.com/share?url=' + get_theme_url(id));
    $('li.share_twitter > a').attr('href', 'http://twitter.com/share?text=Firefox自製佈景主題&url=' + get_theme_url(id));
    $('li.share_pinterest > a').attr('href', 'http://pinterest.com/pin/create/button/?media=' + get_theme_url(id));
  }

  function get_theme_url(id) {
    return "https://" + window.location.hostname + "/thememaker/theme/" + id;  
  }
}

function slider_listener() {
  $($("#cover_list > ul > li").get(0)).children('a').addClass('on');
  var color = $($('li.item').get(0)).children('div.demo_section').children('span.demo_mask').attr('color');
  $('div#main_cover').addClass(color);

  var slider = $("#cover_ul");

  slider.owlCarousel({
    slideSpeed : 300,
    paginationSpeed : 400,
    singleItem: true,
    pagination: false,
    autoPlay: 3000,
    stopOnHover: true,
    afterMove: function(){
      var that = this;
      update_slider_status(that.currentItem);
    },
  });

  $(".cover_next").on('click', function(e) {
    e.preventDefault();
    slider.trigger('owl.next');
  });

  $(".cover_pre").on('click', function(e) {
    e.preventDefault();
    slider.trigger('owl.prev');
  });

  // slider_pagination
  $("#cover_list > ul > li").on('click', function(e){
    var $that = $(this);
    e.preventDefault();
    var slider = $("#cover_ul").data('owlCarousel');
    var index = $that.index();
    slider.goTo(index);
  });

  function update_slider_status(pos) {
    var dot = $("#cover_list > ul > li").get(pos);
    var item = $('li.item').get(pos);
    var color = $(item).children('div.demo_section').children('span.demo_mask').attr('color');
    $('div#main_cover').removeClass('Whitecolor Redcolor Yellowcolor Greencolor Bluecolor');
    $('div#main_cover').addClass(color);
    $("#cover_list > ul > li > a").removeClass('on');
    $(dot).children('a').addClass('on');
  }

}