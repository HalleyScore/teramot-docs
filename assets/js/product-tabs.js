// The product docs link to headings that the site turns into tabs, and so does
// search_docs, which answers with those links. Open the tab holding the anchor.
(function () {
  function openTabOfHash() {
    var id = decodeURIComponent(window.location.hash.slice(1));
    var target = id && document.getElementById(id);
    var panel = target && target.closest('[role="tabpanel"]');
    if (!panel) return;
    var tab = document.getElementById(panel.getAttribute("aria-labelledby"));
    if (tab && tab.getAttribute("aria-selected") !== "true") tab.click();
    target.scrollIntoView();
  }
  window.addEventListener("hashchange", openTabOfHash);
  window.addEventListener("load", openTabOfHash);
})();
