"use strict";

$(function() {
    infinitescroll_listener();
    slider_listener();
    expand_theme_listener();
    install_theme_listener();
});

function infinitescroll_listener() {
    $('#theme_container').infinitescroll({
        navSelector: '#page-nav',
        nextSelector: '#page-nav > a',
        itemSelector: '#theme_container ul.theme_block',
        //debug: true,
        loadingImg: '',
        loadingText: '',
        donetext: '',
        animate: true
    }, function() {
        expand_theme_listener();
        install_theme_listener();
    });
}

function install_theme_listener() {
  // TODO: install theme
}

function expand_theme_listener() {
  $('div.theme_bottom_btn > a.expand').unbind();
  $('div.theme_bottom_btn > a.expand').on('click', function(e){
    e.preventDefault();
    var isOpen = $(this).hasClass('on');
    var li_tag = $(this).parent().parent();
    var ul_tag = $(this).parent().parent().parent();
    var li_idx = $(ul_tag).children('li').index(li_tag) + 1;
    $('div.theme_bottom_btn > a.expand').removeClass('on');
    $('#theme_detail').slideUp(400, function(){
      $('#expand_arrow').removeClass('arrow01 arrow02 arrow03').addClass('arrow0' + li_idx);  
      $(ul_tag).after($('#theme_detail'));
      fill_data(li_tag);
    });
    if (!isOpen) {
      $(this).addClass('on');
      $('#theme_detail').slideDown(400);
    }   
  });

  $('a.btn_close').unbind();
  $('a.btn_close').on('click', function(e){
    e.preventDefault();
    $('#theme_detail').slideUp(400);
    $('div.theme_bottom_btn > a.expand').removeClass('on');
  });

  // fill data into #theme_detail element
  function fill_data(ele) {
    var p_tag = ele.children('p.tab_type');
    var meta_title = ele.children('h3').text();
    var meta_desc = ele.children('p.meta_desc').text();
    var meta_date = p_tag.children('span.type_latest').text();
    var meta_download = p_tag.children('span.type_hot').text();
    var meta_likes = p_tag.children('span.type_favorite').text();

    $('#theme_detail_panel h3').text(meta_title);
    $('#theme_detail_panel p').text(meta_desc);
    $('#theme_detail_panel ul li.info_date').text(meta_date);
    $('#theme_detail_panel ul li.info_download').text(meta_download);
    $('#theme_detail_panel ul li.info_fb').text(meta_likes);

  }
}

function slider_listener() {
  $($("#cover_list > ul > li").get(0)).children('a').addClass('on');

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
      e.preventDefault();
      var slider = $("#cover_ul").data('owlCarousel');
      var index = $(this).index();
      slider.goTo(index);
  });

  function update_slider_status(pos) {
      $("#cover_list > ul > li > a").removeClass('on');
      $($("#cover_list > ul > li").get(pos)).children('a').addClass('on');
  }
}

