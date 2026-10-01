// The product docs link to headings that the site turns into tabs, and so does
// search_docs, which answers with those links. Open the tab holding the anchor.
(function () {
  function openTabOfHash() {
    var id = decodeURIComponent(window.location.hash.slice(1));
    var target = id && document.getElementById(id);
    var panel = target && target.closest('[role="tabpanel"]');
    if (!panel) return;
    var tab = document.getElementById(panel.getAttribute("aria-labelledby"));
    if (!tab) return;
    if (tab.getAttribute("aria-selected") !== "true") tab.click();
    // The tab bar, not the anchor inside the panel, so the reader sees which tab opened;
    // a bar wider than the page also scrolls sideways to that tab.
    var bar = tab.closest(".hextra-scrollbar") || tab;
    bar.scrollIntoView();
    bar.scrollLeft += tab.getBoundingClientRect().left - bar.getBoundingClientRect().left - 16;
  }
  window.addEventListener("hashchange", openTabOfHash);
  window.addEventListener("load", openTabOfHash);
})();
