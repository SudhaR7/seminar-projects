// ===== TechVerse 2026 — JavaScript = the BRAIN of the page =====
const $ = (id) => document.getElementById(id);
const store = {
  get(k, d) { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
};

// 1) Toast message
function toast(msg) {
  const t = $("toast");
  t.textContent = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 2500);
}

// 2) Dark / Light theme (remembered after refresh)
function applyTheme(light) {
  document.body.classList.toggle("light", light);
  $("themeBtn").textContent = light ? "☀️ Light" : "🌙 Dark";
}
applyTheme(store.get("light", false));
$("themeBtn").onclick = () => {
  const light = !document.body.classList.contains("light");
  applyTheme(light);
  store.set("light", light);
};

// 3) Typing effect with rotating words
const words = ["Web Developer", "Python Pro", "Data Scientist", "AI Engineer", "Startup Founder"];
let wi = 0, ci = 0, deleting = false;
(function type() {
  const word = words[wi];
  $("typing").textContent = word.slice(0, ci);
  if (!deleting && ci < word.length) ci++;
  else if (deleting && ci > 0) ci--;
  else { deleting = !deleting; if (!deleting) wi = (wi + 1) % words.length; }
  setTimeout(type, deleting ? 50 : ci === word.length ? 1400 : 110);
})();

// 4) Live countdown (to 7 days from first visit — always looks "live" in a demo)
let target = store.get("target", null);
if (!target || target < Date.now()) { target = Date.now() + 7 * 864e5; store.set("target", target); }
setInterval(() => {
  const diff = Math.max(0, target - Date.now());
  $("d").textContent = Math.floor(diff / 864e5);
  $("h").textContent = Math.floor(diff / 36e5) % 24;
  $("m").textContent = Math.floor(diff / 6e4) % 60;
  $("s").textContent = Math.floor(diff / 1e3) % 60;
}, 1000);

// 5) Scroll reveal + animated counters
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (!e.isIntersecting) return;
    e.target.classList.add("show");
    e.target.querySelectorAll("[data-count]").forEach((el) => {
      const end = +el.dataset.count; let n = 0;
      const step = Math.ceil(end / 60);
      const t = setInterval(() => { n = Math.min(end, n + step); el.textContent = n; if (n === end) clearInterval(t); }, 25);
    });
    io.unobserve(e.target);
  });
}, { threshold: 0.2 });
document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

// 6) Clickable track cards
document.querySelectorAll(".card").forEach((c) =>
  c.addEventListener("click", () => {
    $("track").value = c.dataset.track;
    toast(`🔥 ${c.dataset.track} selected! Scroll down to register`);
    $("register").scrollIntoView();
  })
);

// 7) Mouse spotlight
document.addEventListener("mousemove", (e) => {
  $("spot").style.left = e.clientX + "px";
  $("spot").style.top = e.clientY + "px";
});

// 8) Form validation + seat booking saved in localStorage
const TOTAL = 50;
let people = store.get("people", []);
function render() {
  $("left").textContent = TOTAL - people.length;
  $("barFill").style.width = (people.length / TOTAL) * 100 + "%";
  $("list").innerHTML = people.map((p, i) => `<li><span>${i + 1}. ${p.name}</span><span>${p.track}</span></li>`).join("");
}
render();

function check(input, errId, ok, msg) {
  $(errId).textContent = ok ? "" : msg;
  input.classList.toggle("bad", !ok);
  input.classList.toggle("good", ok);
  return ok;
}
$("form").addEventListener("submit", (e) => {
  e.preventDefault();
  const name = $("name").value.trim(), email = $("email").value.trim(), track = $("track").value;
  const ok =
    check($("name"), "nameErr", name.length >= 3, "Name must be at least 3 letters") &
    check($("email"), "emailErr", /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(email), "Enter a valid email") &
    check($("track"), "trackErr", !!track, "Please pick a track");
  if (!ok) return toast("⚠️ Please fix the errors");
  if (people.some((p) => p.email.toLowerCase() === email.toLowerCase())) return toast("😅 This email is already registered");
  if (people.length >= TOTAL) return toast("😢 House full!");
  people.push({ name: name.replace(/[<>]/g, ""), email, track });
  store.set("people", people);
  render();
  e.target.reset();
  document.querySelectorAll("input").forEach((i) => i.classList.remove("good"));
  toast(`🎉 Welcome aboard, ${name}!`);
  confetti();
});
$("reset").onclick = (e) => { e.preventDefault(); people = []; store.set("people", people); render(); toast("Demo reset"); };

// 9) Confetti burst
function confetti() {
  const colors = ["#7c5cff", "#00d4ff", "#ff4fa3", "#ffd23f", "#2bd67b"];
  for (let i = 0; i < 120; i++) {
    const c = document.createElement("div");
    c.className = "confetti";
    c.style.left = Math.random() * 100 + "vw";
    c.style.background = colors[i % colors.length];
    c.style.animationDuration = 2 + Math.random() * 2 + "s";
    document.body.appendChild(c);
    setTimeout(() => c.remove(), 4200);
  }
}
