(function () {
  const init = () => {
    if (!window.mermaid) return;

    window.mermaid.initialize({
      startOnLoad: false,
      theme: "default",
    });

    window.mermaid.run({ querySelector: ".mermaid" });
  };

  document.addEventListener("DOMContentLoaded", init);

  if (window.document$) {
    window.document$.subscribe(() => init());
  }
})();
