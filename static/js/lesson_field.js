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
    $('#btn-format').click(function() {
        var start = editor.getValue();
        var tidied = tidy_html5(start,tidy_opts);
        if (start == tidied) {
            tidied = "<!-- formatter made no changes: check for invalid tags -->\n" + tidied;
        }
        editor.setValue(tidied);
    })

    editor.setOption("extraKeys", {
      Esc: function(cm) {
        cm.setOption('fullScreen',false);
      }
    });


});
