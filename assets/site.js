// Mobile menu toggle
(function () {
  var btn = document.getElementById("menu-toggle");
  var nav = document.getElementById("mobile-nav");
  if (!btn || !nav) return;
  btn.addEventListener("click", function () {
    var open = btn.getAttribute("aria-expanded") !== "true";
    btn.setAttribute("aria-expanded", String(open));
    btn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    nav.classList.toggle("is-open", open);
  });
})();

// Project filters on /projects
(function () {
  var group = document.getElementById("project-filters");
  if (!group) return;
  var buttons = group.querySelectorAll("button");
  var cards = document.querySelectorAll("#project-grid [data-category]");
  var count = document.getElementById("project-count");
  var toggle = document.getElementById("filter-toggle");
  var current = document.getElementById("filter-current");
  function setOpen(open) {
    if (!toggle) return;
    toggle.setAttribute("aria-expanded", String(open));
    group.classList.toggle("is-open", open);
  }
  if (toggle) toggle.addEventListener("click", function () {
    setOpen(toggle.getAttribute("aria-expanded") !== "true");
  });
  buttons.forEach(function (b) {
    b.addEventListener("click", function () {
      var filter = b.getAttribute("data-filter");
      var shown = 0;
      buttons.forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
      cards.forEach(function (c) {
        var match = filter === "all" || c.getAttribute("data-category").split("|").indexOf(filter) !== -1;
        c.style.display = match ? "" : "none";
        if (match) shown++;
      });
      if (count) count.textContent = shown + (shown === 1 ? " project" : " projects");
      if (current) current.textContent = b.textContent;
      if (toggle && toggle.getAttribute("aria-expanded") === "true") {
        setOpen(false);
        if (count) count.scrollIntoView({ block: "start" });
      }
    });
  });
})();
