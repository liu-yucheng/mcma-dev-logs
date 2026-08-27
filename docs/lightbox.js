/* Shared lightbox for all pages. Adds zoom, pan, reset, and close. */
(function () {
  var overlay, imgEl, captionEl, scaleEl;
  var scale = 1, tx = 0, ty = 0;
  var dragging = false, startX = 0, startY = 0, startTx = 0, startTy = 0;

  function apply() {
    imgEl.style.transform =
      "translate(" + tx + "px," + ty + "px) scale(" + scale + ")";
    scaleEl.textContent = Math.round(scale * 100) + "%";
  }

  function changeScale(delta) {
    scale = Math.min(5, Math.max(0.25, scale + delta));
    apply();
  }

  function reset() {
    scale = 1;
    tx = 0;
    ty = 0;
    apply();
  }

  function close() {
    overlay.classList.remove("open");
    document.body.classList.remove("lb-open");
  }

  function open(src, alt, caption) {
    imgEl.src = src;
    imgEl.alt = alt || "";
    captionEl.textContent = caption || "";
    reset();
    overlay.classList.add("open");
    document.body.classList.add("lb-open");
  }

  function build() {
    overlay = document.createElement("div");
    overlay.className = "lb-overlay";
    overlay.innerHTML =
      '<div class="lb-bar">' +
        '<span class="lb-scale">100%</span>' +
        '<button type="button" class="lb-btn" data-act="zoomout" aria-label="Zoom out">-</button>' +
        '<button type="button" class="lb-btn" data-act="reset" aria-label="Reset zoom">1:1</button>' +
        '<button type="button" class="lb-btn" data-act="zoomin" aria-label="Zoom in">+</button>' +
        '<button type="button" class="lb-btn lb-close" data-act="close" aria-label="Close">&#10005;</button>' +
      '</div>' +
      '<div class="lb-stage"></div>' +
      '<p class="lb-caption"></p>';
    document.body.appendChild(overlay);

    var stage = overlay.querySelector(".lb-stage");
    imgEl = document.createElement("img");
    imgEl.className = "lb-img";
    imgEl.draggable = false;
    stage.appendChild(imgEl);
    captionEl = overlay.querySelector(".lb-caption");
    scaleEl = overlay.querySelector(".lb-scale");

    overlay.querySelectorAll("button[data-act]").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.stopPropagation();
        var act = btn.getAttribute("data-act");
        if (act === "close") close();
        else if (act === "zoomin") changeScale(0.25);
        else if (act === "zoomout") changeScale(-0.25);
        else if (act === "reset") reset();
      });
    });

    overlay.addEventListener("click", function (e) {
      if (e.target === overlay || e.target === stage) close();
    });

    overlay.addEventListener("wheel", function (e) {
      e.preventDefault();
      changeScale(e.deltaY < 0 ? 0.15 : -0.15);
    }, { passive: false });

    stage.addEventListener("mousedown", function (e) {
      dragging = true;
      startX = e.clientX;
      startY = e.clientY;
      startTx = tx;
      startTy = ty;
      e.preventDefault();
    });

    document.addEventListener("mousemove", function (e) {
      if (!dragging) return;
      tx = startTx + (e.clientX - startX);
      ty = startTy + (e.clientY - startY);
      apply();
    });

    document.addEventListener("mouseup", function () {
      dragging = false;
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
      else if (e.key === "+" || e.key === "=") changeScale(0.25);
      else if (e.key === "-" || e.key === "_") changeScale(-0.25);
      else if (e.key === "0") reset();
    });
  }

  build();

  document.addEventListener("click", function (e) {
    var target = e.target;
    if (!target.classList || !target.classList.contains("zimg")) return;
    e.preventDefault();
    var figure = target.closest("figure");
    var capNode = figure ? figure.querySelector("figcaption") : null;
    open(target.currentSrc || target.src, target.alt, capNode ? capNode.textContent.trim() : "");
  });
})();