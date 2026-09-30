/*
 * View counts for blog posts.
 *
 * layouts/_partials/teramot/post-meta.html renders a hidden
 * <span class="tm-views"><span data-views-path="/blog/x/"></span> views</span>
 * per post. We fill it from GoatCounter's public counter endpoint, which needs
 * "Allow adding visitor counts on your website" enabled on the site settings.
 * GoatCounter: no cookies, no personal data, and nothing for us to operate.
 *
 * The widget stays hidden unless a real number comes back.
 */
(function () {
  "use strict";

  var cfg = {};
  try {
    var el = document.getElementById("engagement-config");
    if (el && el.textContent) cfg = JSON.parse(el.textContent);
  } catch (e) {
    /* malformed config: treated as unconfigured below */
  }

  var code = (cfg.goatcounterCode || "").trim();
  var nodes = document.querySelectorAll("[data-views-path]");
  if (!code || !nodes.length) return;

  Array.prototype.forEach.call(nodes, function (node) {
    // GoatCounter documents the literal path here (yielding a double slash
    // after /counter/), so escape everything except the separators.
    var path = node.getAttribute("data-views-path");
    var url =
      "https://" +
      code +
      ".goatcounter.com/counter/" +
      encodeURIComponent(path).replace(/%2F/g, "/") +
      ".json";

    fetch(url, { mode: "cors" })
      .then(function (r) {
        // GoatCounter answers 404 for a path it has never recorded, but still
        // sends a usable {"count":"0"} body. A brand new post has no views yet,
        // so that is a real zero. Anything else is genuinely broken.
        if (!r.ok && r.status !== 404) throw new Error("counter " + r.status);
        return r.json();
      })
      .then(function (d) {
        node.textContent = d.count_unique || d.count || "0";
        node.parentElement.hidden = false;
      })
      .catch(function () {
        // Offline, DNS failure, or blocked by an extension: keep it hidden
        // rather than showing a number we cannot stand behind.
      });
  });
})();
