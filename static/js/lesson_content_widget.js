function launchIntoFullscreen(element) {
  if(element.requestFullscreen) {
    element.requestFullscreen();
  } else if(element.mozRequestFullScreen) {
    element.mozRequestFullScreen();
  } else if(element.webkitRequestFullscreen) {
    element.webkitRequestFullscreen();
  } else if(element.msRequestFullscreen) {
    element.msRequestFullscreen();
  }
}

function exitFullscreen() {
  if(document.exitFullscreen) {
    document.exitFullscreen();
  } else if(document.mozCancelFullScreen) {
    document.mozCancelFullScreen();
  } else if(document.webkitExitFullscreen) {
    document.webkitExitFullscreen();
  }
}

function fullscreenElement() {return document.fullscreenElement || document.mozFullScreenElement || document.webkitFullscreenElement; }
function fullscreenEnabled() { return document.fullscreenEnabled || document.mozFullScreenEnabled || document.webkitFullscreenEnabled; }

function insertImageSelection() {
    console.log(grp.jQuery('#id_editor_image').val());
}

grp.jQuery(document).ready(function() {

    tidy_opts = { // http://tidy.sourceforge.net/docs/quickref.html
        "indent": "auto",
        "indent-spaces": 2,
        "markup": true,
        "output-xml": false,
        "numeric-entities": false,
        "quote-marks": true,
        "quote-nbsp": false,
        "show-body-only": true,
        "quote-ampersand": false,
        "break-before-br": true,
        "uppercase-tags": false,
        "uppercase-attributes": false,
        "drop-font-tags": true,
        "tidy-mark": false,
        "show-warnings": false,
        "new-blocklevel-tags": ['lesson-ref', 'step-block', 'narrative-text', 'zooming-image', 'lesson-block', 'capsule-unit', 'media-group', 'info-block'],
        "new-pre-tags": ['code-block'],
        "new-inline-tags": ['glossary-term']
    }

    var editor = CodeMirror.fromTextArea(document.getElementById('messageBody'), {
      mode: 'htmlmixed',
      lineNumbers: true,
      lineWrapping: true
    });

    window.lessonContentEditor = editor;
    var $ = grp.jQuery;

    $('.CodeMirror').resizable({ // http://stackoverflow.com/a/13979570/102476
      resize: function() {
        editor.setSize($(this).width(), $(this).height());
      }
    });

    if (localStorage.getItem('lcw-codemirror-font-size')) {
      $('.CodeMirror').css('font-size', localStorage.getItem('lcw-codemirror-font-size'));
    }

    $(function() {
        $.getJSON('/lesson_json', function(data) {
            $.each(data, function(lesson, info) {
                if (info.status == "draft") {
                    $('.lesson-chosen-select').append('<option class="draft" value="' + info.slug + '">' + lesson + '</option>');
                } else {
                    $('.lesson-chosen-select').append('<option value="' + info.slug + '">' + lesson + '</option>');
                } 
            });
            $('.lesson-chosen-select').chosen({
                max_selected_options: 1,
                width: '95%'
            });
        });

        $('#search-lessons').dialog({
            autoOpen: false
        });
    });

    $(function() {
        $.getJSON('/capsule_json', function(data) {
            $.each(data, function(capsule, slug) {
                $('.capsule-chosen-select').append('<option value="' + slug + '">' + capsule + '</option>');
            });
            $('.capsule-chosen-select').chosen({
                max_selected_options: 1,
                width: '95%'
            });
        });

        $('#search-capsules').dialog({
            autoOpen: false
        });
    });

    $(".lesson-chosen-select").change(function(e, params) {
        var lesson_name = params.selected;
        $('#search-lessons').dialog('close');
        editor.replaceSelection('<lesson-ref ref="' + lesson_name + '"></lesson-ref>');
        editor.focus();
    });
    $(".capsule-chosen-select").change(function(e, params) {
        var capsule_name = params.selected;
        $('#search-capsules').dialog('close');
        editor.replaceSelection('<capsule-unit ref="' + capsule_name + '"></capsule-unit>');
        editor.focus();
    });

    $('#btn-narrative-text').click(function() {
        var cursor = editor.getCursor();
        var note = '\t<!-- narrative-text can contain any HTML markup. It typically occurs once at the top of a lesson.-->';
        editor.replaceSelection('<narrative-text>\n'+note+'\n</narrative-text>\n');
        editor.setSelection({line: cursor.line + 1, ch: 1},{line: cursor.line+1, ch: note.length});
        editor.focus();
    })
    $('#btn-lesson-block').click(function() {
        editor.replaceSelection('<lesson-block header="">\n</lesson-block>\n');
        editor.focus();
    })
    $('#btn-step-block').click(function() {
        editor.replaceSelection('<step-block header="">\n</step-block>\n');
        editor.focus();
    })
    $('#btn-info-block').click(function() {
        editor.replaceSelection('<info-block emoji="&#x2757;" header="">\n</info-block>\n');
        editor.focus();
    })
    $('#btn-capsule-unit').click(function() {
        $('#search-capsules').dialog('open');
    })
    $('#btn-zooming-image').click(function() {
        editor.replaceSelection('<zooming-image ref="">\n</zooming-image>\n');
        editor.focus();
    })
    $('#btn-code-block').click(function() {
        editor.replaceSelection('<code-block>\n</code-block>\n');
        editor.focus();
    });
    $('#btn-glossary-term').click(function() {
        editor.replaceSelection('<glossary-term>' + editor.getSelection() + '</glossary-term>');
        editor.focus();
    });
    $('#btn-lesson-ref').click(function() {
        $('#search-lessons').dialog('open');
    });
    $('#btn-font-larger').click(function() {
        var size = parseFloat($('.CodeMirror').css('font-size'));
        var newSize = (size + .5) + "px";
        localStorage.setItem('lcw-codemirror-font-size', newSize);
        $('.CodeMirror').css('font-size', newSize);
    });
    $('#btn-font-smaller').click(function() {
      var size = parseFloat($('.CodeMirror').css('font-size'));
      var newSize = (size - .5) + "px";
      localStorage.setItem('lcw-codemirror-font-size', newSize);
      $('.CodeMirror').css('font-size', newSize);
    });

    $('#btn-fullscreen').click(function() {
      if (editor.getOption('fullScreen')) {
        exitFullscreen();
      } else {
        editor.setOption('fullScreen', true);
      }
    })

    $('#btn-format').click(function() {
        var start = editor.getValue();
        var tidied = tidy_html5(start,tidy_opts);
        if (start == tidied) {
            tidied = "<!-- formatter made no changes: check for invalid tags -->\n" + tidied;
        }
        editor.setValue(tidied);
        editor.setCursor({line: 0, ch: 0});
        editor.focus();

    })

    editor.setOption("extraKeys", {
      Esc: function(cm) {
        cm.setOption('fullScreen',false);
      }
    });


});
