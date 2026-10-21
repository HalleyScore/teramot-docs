// Copy of themes/hextra/assets/js/core/sidebar.js (overrides it in the js/core bundle);
// the only change is the early return in scrollToActiveItem.

document.addEventListener("DOMContentLoaded", function () {
  scrollToActiveItem();
  enableCollapsibles();
});

function enableCollapsibles() {
  const buttons = document.querySelectorAll(".hextra-sidebar-collapsible-button");
  buttons.forEach(function (button) {
    button.addEventListener("click", function (e) {
      e.preventDefault();
      const list = button.closest('li');
      if (list) {
        list.classList.toggle("open");
        button.setAttribute('aria-expanded', list.classList.contains('open') ? 'true' : 'false');
      }
    });
  });
}

function scrollToActiveItem() {
  const sidebarScrollbar = document.querySelector("aside.hextra-sidebar-container > .hextra-scrollbar");
  const activeItems = document.querySelectorAll(".hextra-sidebar-active-item");
  const visibleActiveItem = Array.from(activeItems).find(function (activeItem) {
    return activeItem.getBoundingClientRect().height > 0;
  });

  if (!visibleActiveItem) {
    return;
  }

  // Teramot: leave the sidebar where it is when the active item is already in view,
  // so opening a section doesn't scroll the sections above it out of reach.
  const itemRect = visibleActiveItem.getBoundingClientRect();
  const scrollRect = sidebarScrollbar.getBoundingClientRect();
  if (itemRect.top >= scrollRect.top && itemRect.bottom <= scrollRect.bottom) {
    return;
  }

  const yOffset = visibleActiveItem.clientHeight;
  const yDistance = itemRect.top - scrollRect.top;
  sidebarScrollbar.scrollTo({
    behavior: "instant",
    top: yDistance - yOffset
  });
}
