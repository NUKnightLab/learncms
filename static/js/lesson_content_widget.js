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
      mode: 'xml',
      lineNumbers: true,
      lineWrapping: true
    });

    window.lessonContentEditor = editor;
    var $ = grp.jQuery;
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
        editor.replaceSelection('<info-block header="">\n</info-block>\n');
        editor.focus();
    })
    $('#btn-capsule-unit').click(function() {
        editor.replaceSelection('<capsule-unit ref="">\n</capsule-unit>\n');
        editor.focus();
    })
    $('#btn-zooming-image').click(function() {
        editor.replaceSelection('<zooming-image ref="">\n</zooming-image>\n');
        editor.focus();
    })
    $('#btn-code-block').click(function() {
        editor.replaceSelection('<code-block>\n</code-block>\n');
        editor.focus();
    });
    // $('#btn-fullscreen').click(function() {
    //     editor.setOption('fullScreen',true);
    // })
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
