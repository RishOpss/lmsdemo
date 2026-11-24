// Sample data: the backend has no courses endpoint yet. Swap for fetch("/api/v1/courses/") later.
const COURSES = [
  { cat: "Development", icon: "🐍", color: "#4f46e5", title: "Python for Beginners", desc: "Learn programming fundamentals with Python.", duration: 20 },
  { cat: "Development", icon: "🌐", color: "#0ea5e9", title: "Web Development Bootcamp", desc: "HTML, CSS and JavaScript from scratch.", duration: 40 },
  { cat: "Development", icon: "⚡", color: "#059669", title: "FastAPI Masterclass", desc: "Build fast async APIs with FastAPI.", duration: 15 },
  { cat: "Data", icon: "📊", color: "#d97706", title: "Data Analysis with Pandas", desc: "Clean, explore and visualize data.", duration: 18 },
  { cat: "Data", icon: "🤖", color: "#7c3aed", title: "Machine Learning Basics", desc: "Core ML concepts and models.", duration: 30 },
  { cat: "Data", icon: "🗄️", color: "#0891b2", title: "SQL Essentials", desc: "Query and design relational databases.", duration: 12 },
  { cat: "Design", icon: "🎨", color: "#db2777", title: "UI/UX Design Fundamentals", desc: "Design intuitive, beautiful interfaces.", duration: 16 },
  { cat: "Design", icon: "✏️", color: "#e11d48", title: "Figma for Beginners", desc: "Prototype apps and websites in Figma.", duration: 10 },
  { cat: "Business", icon: "📈", color: "#16a34a", title: "Digital Marketing 101", desc: "SEO, ads and social media strategy.", duration: 14 },
  { cat: "Business", icon: "💼", color: "#475569", title: "Project Management", desc: "Plan and deliver projects on time.", duration: 22 },
];
const cats = ["All", ...new Set(COURSES.map((c) => c.cat))];
const tabsEl = document.getElementById("tabs");
const gridEl = document.getElementById("courses");

function show(cat) {
  tabsEl.querySelectorAll(".tab").forEach((t) => t.setAttribute("aria-selected", t.textContent === cat));
  gridEl.replaceChildren(...COURSES.filter((c) => cat === "All" || c.cat === cat).map(card));
}

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined) e.textContent = text;
  return e;
}

function card(c) {
  const art = el("article", "course");
  const thumb = el("div", "thumb", c.icon);
  thumb.style.background = `color-mix(in srgb, ${c.color} 22%, transparent)`;
  const body = el("div", "body");
  body.append(el("h3", "", c.title), el("p", "", c.desc), el("span", "meta", `${c.cat} · ${c.duration} hours`));
  art.append(thumb, body);
  return art;
}

cats.forEach((cat) => {
  const b = el("button", "tab", cat);
  b.type = "button";
  b.role = "tab";
  b.addEventListener("click", () => show(cat));
  tabsEl.append(b);
});
show("All");

// Dialogs
const signup = document.getElementById("signup");
const signin = document.getElementById("signin");
document.querySelectorAll("[data-close]").forEach((b) => (b.onclick = () => b.closest("dialog").close()));

function msg(id, text, cls) {
  const m = document.getElementById(id);
  m.textContent = text;
  m.className = "msg " + (cls || "");
}

document.getElementById("signup-form").addEventListener("submit", async (e) => {
  e.preventDefault(); // keep dialog open until the request finishes
  const data = Object.fromEntries(new FormData(e.target));
  msg("signup-msg", "Creating account…");
  try {
    const res = await fetch("/api/v1/users/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(await errorMessage(res, "signup"));
    msg("signup-msg", "Account created! You can sign in now.", "ok");
    e.target.reset();
    setTimeout(() => { signup.close(); msg("signup-msg", ""); }, 1200);
  } catch (err) {
    msg("signup-msg", networkMessage(err), "error");
  }
});

document.getElementById("signin-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target));
  msg("signin-msg", "Signing in…");
  try {
    const res = await fetch("/api/v1/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(await errorMessage(res, "signin"));
    Session.set(await res.json());
    e.target.reset();
    msg("signin-msg", "");
    signin.close();
    renderAuth();
  } catch (err) {
    msg("signin-msg", networkMessage(err), "error");
  }
});

// Top-right: sign in/up buttons, or the profile avatar once signed in.
function renderAuth() {
  const auth = document.getElementById("auth");
  const user = Session.get();
  if (!user) {
    const inB = el("button", "btn ghost", "Sign in"), upB = el("button", "btn", "Sign up");
    inB.type = upB.type = "button";
    inB.onclick = () => signin.showModal();
    upB.onclick = () => signup.showModal();
    auth.replaceChildren(inB, upB);
    return;
  }
  const a = el("a", "profile-link");
  a.href = "profile.html";
  a.title = `${user.username} – view profile`;
  a.append(Session.avatar(user));
  auth.replaceChildren(a);
}
renderAuth();
