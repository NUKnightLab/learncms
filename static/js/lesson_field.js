
function insertAtCaret(areaId,text) {
 var txtarea = document.getElementById(areaId);
 var scrollPos = txtarea.scrollTop;
 var strPos = 0;
 var br = ((txtarea.selectionStart || txtarea.selectionStart == '0') ?
   "ff" : (document.selection ? "ie" : false ) );
 if (br == "ie") {
   txtarea.focus();
   var range = document.selection.createRange();
   range.moveStart ('character', -txtarea.value.length);
   strPos = range.text.length;
 }
 else if (br == "ff") strPos = txtarea.selectionStart;

 var front = (txtarea.value).substring(0,strPos);
 var back = (txtarea.value).substring(strPos,txtarea.value.length);
 txtarea.value=front+text+back;
 strPos = strPos + text.length;
 if (br == "ie") {
   txtarea.focus();
   var range = document.selection.createRange();
   range.moveStart ('character', -txtarea.value.length);
   range.moveStart ('character', strPos);
   range.moveEnd ('character', 0);
   range.select();
 }
 else if (br == "ff") {
   txtarea.selectionStart = strPos;
   txtarea.selectionEnd = strPos;
   txtarea.focus();
 }
 txtarea.scrollTop = scrollPos;
}

grp.jQuery(document).ready(function() {
    var editor = CodeMirror.fromTextArea(document.getElementById('messageBody'), {
      mode: 'xml',
      lineNumbers: true
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
});
