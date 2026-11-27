// Shared session helpers. The backend has no tokens yet, so the user object lives in localStorage.
const Session = {
  get() { try { return JSON.parse(localStorage.getItem("lms_user")); } catch { return null; } },
  set(u) { localStorage.setItem("lms_user", JSON.stringify(u)); },
  clear() { localStorage.removeItem("lms_user"); },
  photo(u) { return localStorage.getItem(`lms_photo_${u.id}`); },
  setPhoto(u, dataUrl) { localStorage.setItem(`lms_photo_${u.id}`, dataUrl); },
  // Round avatar: uploaded photo if present, otherwise the user's initial.
  avatar(u, cls = "avatar") {
    const el = document.createElement("span");
    el.className = cls;
    const p = Session.photo(u);
    if (p) { el.style.backgroundImage = `url(${p})`; }
    else { el.textContent = (u.username || "?")[0].toUpperCase(); }
    return el;
  },
};

// Turn any failed response / thrown error into a readable message.
async function errorMessage(res, context) {
  const text = await res.text().catch(() => "");
  let detail;
  try { detail = JSON.parse(text).detail; } catch { /* non-JSON body, e.g. plain "Internal Server Error" */ }

  if (Array.isArray(detail)) { // FastAPI validation errors
    return detail.map((d) => `${String(d.loc.at(-1)).replace("_", " ")}: ${d.msg}`).join("\n");
  }
  if (typeof detail === "string") {
    const m = detail.toLowerCase();
    if (/duplicate|unique|already exists|violates/.test(m)) return "That username, email or phone number is already registered.";
    return detail;
  }
  if (res.status === 409) return "That username, email or phone number is already registered.";
  if (res.status === 500 && context === "signup")
    return "Could not create the account (server error). The username, email or phone number is probably already registered.";
  if (res.status >= 500) return `Server error (${res.status}). Please try again later.`;
  return `Request failed (${res.status}).`;
}

function networkMessage(err) {
  return err instanceof TypeError ? "Cannot reach the server. Check your connection and try again." : err.message;
}
