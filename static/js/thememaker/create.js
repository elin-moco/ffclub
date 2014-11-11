"use strict";

$(function() {
  input_listener();
  template_theme_slider();
  drag_image_listener();
});

function input_listener() {
  $('input').on('focus', function(){
    $(this).removeClass('error');
  });
  $('textarea').on('focus', function(){
    $(this).removeClass('error');
  });
}

function drag_image_listener() {
  var canvas = new fabric.Canvas('pic_canvas');
  canvas.setHeight(300);
  canvas.setWidth(1000);

  var holder = document.getElementById('upload_area'),
  tests = {
    filereader: typeof FileReader != 'undefined',
    dnd: 'draggable' in document.createElement('span'),
    formdata: !!window.FormData,
    progress: "upload" in new XMLHttpRequest
  }, 
  acceptedTypes = {
    'image/png': true,
    'image/jpeg': true,
    'image/gif': true
  },
  progress = $('#uploadprogress'),
  fileupload = $('#upload');

  holder.ondragover = function () { return false; };
  holder.ondragend = function () { return false; };
  holder.ondrop = function (e) {
    e.preventDefault();
    read_files(e.dataTransfer.files, canvas);
  }

  $('#upload_field').on('change', function(){
    read_files(this.files, canvas);
  });

  submit_form_listener(canvas);

  function add_image_on_panel(ifile, canvasPanel) {
    canvasPanel.clear().renderAll();
    fabric.Image.fromURL(ifile, function(img) {
      var oImg = img.set({ left: 50, top: 100, angle: -15 }).scaleToWidth(600);
      canvasPanel.add(oImg).renderAll();
      canvasPanel.setActiveObject(oImg);
    });
  }

  function is_valid_input() {
    var title = $.trim($('input[name="title"]').val());
    var description = $.trim($('textarea[name="description"]').val());
    if((title=="") || (description=="")) {
      $('input').addClass('error');
      $('textarea').addClass('error');
      return false;  
    }
    return true;
  }

  function submit_form_listener(canvasPanel) {
    $('#btn_section a').on('click', function(e){
      e.preventDefault();
      
      if(!is_valid_input()) {
        return false;
      }

      if(canvasPanel.item(0) === undefined) {
        $('#upload_area').text('您尚未上傳任何圖片');
        return false;
      }

      canvasPanel.item(0)['hasControls'] = false;
      canvasPanel.item(0)['hasBorders'] = false;

      canvasPanel.renderAll();
      var dataURI = canvasPanel.toDataURL();
      $('#user_image').val(dataURI);
      $('input#template_id').val($('ul#theme_Canned li a.on').attr('data-id'));

      canvasPanel.item(0)['hasControls'] = true;
      canvasPanel.item(0)['hasBorders'] = true;

      $('#step_sectionthird form').submit();
    });
  }

  function read_files(files, canvasPanel) {
    var formData = tests.formdata ? new FormData() : null;
    for (var i = 0; i < files.length; i++) {
      if (tests.formdata) {
        formData.append('file', files[i]);
        preview_file(files[i], canvasPanel);
        $('#upload_area').text('圖片上傳成功，亦可重新上傳更換圖片');
      } else {
        $('#upload_area').text('圖片上傳失敗，請再試試');
      }
    }
  }

  function preview_file(file, canvasPanel) {
    if (tests.filereader === true && acceptedTypes[file.type] === true) {
      var reader = new FileReader();
      reader.onload = function (event) {
        add_image_on_panel(event.target.result, canvasPanel);
      };
      reader.readAsDataURL(file);
    }  
  }
}

function template_theme_slider() {
  var ITEM_PER_LIST = 8;
  var slider = $('#theme_Canned');

  slider.owlCarousel({
    items : ITEM_PER_LIST, 
    itemsDesktop : [1000,5],
    itemsMobile : false,
    afterMove: moved
  });

  var slider_obj = $('#theme_Canned').data('owlCarousel');

  // initial selected
  $('ul#next_theme li:first a').addClass('on');
  set_template_image($('ul#theme_Canned li:first a'));   

   // template themes
   $('ul#theme_Canned li').on('click', function(e){
    e.preventDefault();
    $('ul#theme_Canned li a').removeClass('on');
    set_template_image($(this).children('a'));
  });

  // pagination
  $('ul#next_theme li').on('click', function(e){
    var index = $(this).index();
    e.preventDefault();
    $('ul#next_theme li a').removeClass('on');
    $(this).children('a').addClass('on');
    slider_obj.goTo(index * ITEM_PER_LIST);
  });

  function moved() {
    var slider_obj = $('#theme_Canned').data('owlCarousel');
    var page = Math.round(((slider_obj.currentItem + 1) / ITEM_PER_LIST) + 1);
    //console.log('item: ' + slider_obj.currentItem + ', page: ' + page);
    $('ul#next_theme li a').removeClass('on');     
    $('ul#next_theme li:nth-child(' + page + ')').children('a').addClass('on');
  }

  function set_template_image(selected_item) {
    selected_item.addClass('on');
    $('.upload_theme img').attr('src', selected_item.attr('href'));
  }
}