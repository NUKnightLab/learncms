grp.jQuery(document).ready(function() {
    var editor = CodeMirror.fromTextArea(document.getElementById('messageBody'), {
      mode: 'xml',
      lineNumbers: true,
      lineWrapping: true
    });

    window.lessonContentEditor = editor;
    var $ = grp.jQuery;
    $('#btn-narrative-text').click(function() {
        editor.replaceRange('<narrative-text>\n</narrative-text>\n',editor.getCursor());
    })
    $('#btn-lesson-block').click(function() {
        editor.replaceRange('<lesson-block>\n</lesson-block>\n',editor.getCursor());
    })
    $('#btn-step-block').click(function() {
        editor.replaceRange('<step-block>\n</step-block>\n',editor.getCursor());
    })
    $('#btn-info-block').click(function() {
        editor.replaceRange('<info-block>\n</info-block>\n',editor.getCursor());
    })
    $('#btn-capsule-unit').click(function() {
        editor.replaceRange('<capsule-unit>\n</capsule-unit>\n',editor.getCursor());
    })
    $('#btn-zooming-image').click(function() {
        editor.replaceRange('<zooming-image>\n</zooming-image>\n',editor.getCursor());
    })
    $('#btn-code-block').click(function() {
        editor.replaceRange('<code-block>\n</code-block>\n',editor.getCursor());
    });
    $('#btn-fullscreen').click(function() {
        editor.setOption('fullScreen',true);
    })

    editor.setOption("extraKeys", {
      Esc: function(cm) {
        cm.setOption('fullScreen',false);
      }
    });


});
