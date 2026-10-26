/* SPDX-License-Identifier: MIT
 *
 * Renders the conceptual models' diagrams on the Models page.
 *
 * The page carries each diagram as its Mermaid source, escaped, inside
 * <pre class="mermaid">: with JavaScript off, that source is what the
 * reader sees, and it is the diagram's truth
 * (docs/decisions/2026-10-25-stage-02-choices.md). This file is loaded
 * after the vendored Mermaid bundle (assets/vendor/mermaid/, pinned in
 * config/site-vendor.yaml) and on no other page.
 *
 * securityLevel "strict" is Mermaid's own guard: labels are sanitised and
 * click handlers are disabled, so diagram text cannot become markup or
 * script. startOnLoad is off and run() is called explicitly, so the
 * diagrams render once, from exactly the elements this page marks.
 */
(function () {
  "use strict";
  if (typeof window.mermaid === "undefined") {
    return; // the source stays readable as text
  }
  // The stylesheet follows prefers-color-scheme; so do the diagrams, or
  // their dark lines would sit on the dark page.
  var dark = window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches;
  window.mermaid.initialize({
    startOnLoad: false,
    securityLevel: "strict",
    theme: dark ? "dark" : "default"
  });
  window.mermaid.run({ querySelector: "pre.mermaid" });
})();
