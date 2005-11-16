if(typeof(Forms) == 'undefined') {
    Forms = {};
}

if(typeof(Forms.ReSTWidget) == 'undefined') {
    Forms.ReSTWidget = {};
}

Forms.ReSTWidget.preview = function(divId, frameId, u) {
    var div = document.getElementById(divId);
    var frame = document.getElementById(frameId);
    div.className = 'preview';
    frame.src = u;
    return false;
}

Forms.ReSTWidget.previewHide = function(divId) {
    var div = document.getElementById(divId);
    div.className = 'preview-hidden';
    return false;
}

