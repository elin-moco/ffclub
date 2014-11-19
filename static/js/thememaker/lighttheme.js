"use strict";

var INSTALL = "InstallBrowserTheme";
var PREVIEW = "PreviewBrowserTheme";
var RESET_PREVIEW = "ResetBrowserThemePreview";

function setTheme(node, theme, action) {
  node.setAttribute("data-browsertheme", JSON.stringify(theme));
  var event = document.createEvent("Events");
  event.initEvent(action, true, false);
  node.dispatchEvent(event);
}