/* ═══ Agahiyên malperê: tenê li vir biguherîne ═══ */
const SITE = {
  name: "GOTAR",
  tagline: "Gotar û lêkolînên bi kurmancî",
  motto: "Zanist · Ziman · Raman"
};

/* Gotar ji articles.js tên xwendin (python3 build.py ew çêdike). */
const ARTICLES = (window.GOTAR || []).slice().sort((a, b) => b.date.localeCompare(a.date));

const $ = s => document.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const norm = s => s.toLocaleLowerCase("tr").normalize("NFD").replace(/[̀-ͯ]/g, "");
const idOf = a => a.id || a.file.split("/").pop().replace(/\.pdf$/i, "");
const pageOf = a => "gotar.html?g=" + encodeURIComponent(idOf(a));
const topicUrl = t => "index.html?mijar=" + encodeURIComponent(t) + "#gotar";

/* Serî û binî li hemû rûpelan yek in */
document.addEventListener("DOMContentLoaded", () => {
  const nav = `
    <a href="index.html">Destpêk</a>
    <a href="index.html#gotar">Gotar</a>
    <a href="index.html#mijar">Mijar</a>
    <a href="derbare.html">Derbarê</a>`;
  const top = document.createElement("header");
  top.className = "top";
  top.innerHTML = `<div class="in">
    <a class="brand" href="index.html"><b>${esc(SITE.name)}</b><span>${esc(SITE.tagline)}</span></a>
    <nav aria-label="Menû">${nav}</nav></div>`;
  document.body.prepend(top);

  const foot = document.createElement("footer");
  foot.innerHTML = `<div class="in">
    <div><b>${esc(SITE.name)}</b><div>${esc(SITE.tagline)}</div><p class="eyebrow">${esc(SITE.motto)}</p></div>
    <nav aria-label="Girêdan">
      <a href="index.html#gotar">Gotar</a><a href="index.html#mijar">Mijar</a>
      <a href="derbare.html">Derbarê</a>
    </nav>
    <p class="copy">© ${new Date().getFullYear()} ${esc(SITE.name)}</p></div>`;
  document.body.append(foot);

  document.querySelectorAll("[data-site-name]").forEach(e => e.textContent = SITE.name);
});
