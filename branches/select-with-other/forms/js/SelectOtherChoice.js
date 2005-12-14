if(typeof(Forms) == 'undefined') {
  throw("Forms.Widget.SelectOtherChoice depends on Forms");
}

if(typeof(Forms.Widget.SelectOtherChoice) == 'undefined') {
  Forms.Widget.SelectOtherChoice = {};
}

if(typeof(MochiKit) == 'undefined' || typeof(MochiKit.DOM) == 'undefined') {
  throw("Forms.Widget.SelectOtherChoice depends on MochiKit.DOM");
}

/**
 * SelectOtherChoice "class".
 */
Forms.Widget.SelectOtherChoice = function(node) {
  // Store reference to main node
  this.node = node;
  // Find the other interesting nodes.
  this.selectNode = MochiKit.DOM.getElementsByTagAndClassName('select', null, this.node)[0];
  var inputs = MochiKit.DOM.getElementsByTagAndClassName('input', null, this.node);
  this.hiddenNode = inputs[0];
  this.otherNode = inputs[1];
}

// The CSS class of the main element
Forms.Widget.SelectOtherChoice.CSS_CLASS = 'select-with-other';

// The value of the "Other ..." option
Forms.Widget.SelectOtherChoice.OTHER_VALUE = '...';

/**
 * Search up the DOM tree, starting with the given node, looking for a node
 * with a the correct tag name and optional class.
 */
Forms.Widget.SelectOtherChoice._getParentElementByTagAndClassName = function(node, tagName, className) {
  tagName = tagName.toUpperCase();
  while(node) {
    if(node.tagName.toUpperCase() == tagName) {
      if(className == undefined || MochiKit.DOM.hasElementClass(node, className)) {
        return node;
      }
    }
    node = node.parentNode;
  }
  return null;
}

/**
 * Get a SelectOtherChoice instance for the current widget.
 */
Forms.Widget.SelectOtherChoice.get = function(node) {
  var widgetNode = Forms.Widget.SelectOtherChoice._getParentElementByTagAndClassName(
    node, 'span',Forms.Widget.SelectOtherChoice.CSS_CLASS);
  return new Forms.Widget.SelectOtherChoice(widgetNode);
}

/*
 * Update the widget state.
 */
Forms.Widget.SelectOtherChoice.prototype._selectChanged = function() {

  // Is the "Other" value currently selected.
  var isOther = (this.selectNode.value == Forms.Widget.SelectOtherChoice.OTHER_VALUE)

  // Disable or enable the input.
  this.otherNode.disabled = !isOther;

  // Add or remove the 'other' class to allow fanciness like hiding the input.
  if(isOther) {
    this.hiddenNode.value = this.otherNode.value;
    addElementClass(this.node, 'other');
  } else {
    this.hiddenNode.value = this.selectNode.value;
    removeElementClass(this.node, 'other');
  }

  // Set the focus to the input if changing to other
  if(isOther) {
    this.otherNode.focus();
  }
}

Forms.Widget.SelectOtherChoice.prototype._otherChanged = function() {
  this.hiddenNode.value = this.otherNode.value;
}

/*
 * Initialise a SelectOtherChoice from its value. This means finding the
 * option to select and fiddling around with the other value input field, etc.
 * 
 * This is *such* a hack. There really needs to be some generic code that
 * instantiates Forms widgets at load time. The widget instances can then
 * be cached for when Widget.get() is called etc.
 */
Forms.Widget.SelectOtherChoice._cheatingSetup = function(id) {
  var widget = new Forms.Widget.SelectOtherChoice(MochiKit.DOM.getElement(id));
  var value = widget.hiddenNode.value;
  // See if the value matches one of the options
  for(var i=0; i<widget.selectNode.options.length; i++) {
    if(value == widget.selectNode.options[i].value) {
      widget.selectNode.selectedIndex = i;
      return;
    }
  }
  // Select the other option, update the other input field, blah blah blah
  widget.selectNode.selectedIndex = widget.selectNode.options.length-1;
  widget.otherNode.value = widget.hiddenNode.value;
  addElementClass(widget.node, 'other');
  widget.otherNode.disabled = false;
  widget.otherNode.focus();
}
