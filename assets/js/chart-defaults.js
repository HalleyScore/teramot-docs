// Chart.js defaults in Teramot colours; charts can still override per dataset.
(function () {
  "use strict";
  var dark = document.documentElement.classList.contains("dark");
  var ink = dark ? "#a5afbf" : "#536071";
  var rule = dark ? "rgba(248, 250, 252, 0.12)" : "rgba(11, 15, 20, 0.1)";

  Chart.defaults.font.size = 14;
  Chart.defaults.color = ink;
  Chart.defaults.borderColor = rule;
  Chart.defaults.backgroundColor = "rgba(37, 61, 229, 0.35)";
  Chart.defaults.elements.point.borderColor = "#5a6df3";
  Chart.defaults.elements.bar.borderColor = "#253de5";
  Chart.defaults.elements.bar.borderWidth = 1;
  Chart.defaults.elements.line.borderColor = "#5a6df3";
  Chart.defaults.elements.arc.backgroundColor = "rgba(37, 61, 229, 0.2)";
  Chart.defaults.elements.arc.borderColor = "#253de5";
  Chart.defaults.elements.arc.borderWidth = 1;
})();
