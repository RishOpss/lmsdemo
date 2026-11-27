const user = Session.get();
if (!user) location.replace("/"); // not signed in

const root = document.getElementById("profile");
const input = document.getElementById("photo-input");

function mk(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined) e.textContent = text;
  return e;
}

function render() {
  const dl = mk("dl");
  [["Username", user.username], ["Email", user.email], ["Phone", user.phone_number],
   ["Member since", new Date(user.created_at).toLocaleDateString()]]
    .forEach(([k, v]) => dl.append(mk("dt", "", k), mk("dd", "", v)));

  const badge = mk("span", `badge ${user.role}`, user.role);
  const wrap = mk("div", "role"); wrap.append(badge);

  const change = mk("button", "btn ghost", "Change photo");
  const signout = mk("button", "btn", "Sign out");
  change.type = signout.type = "button";
  change.onclick = () => input.click();
  signout.onclick = () => { Session.clear(); location.href = "/"; };
  const row = mk("div", "row"); row.append(change, signout);

  root.replaceChildren(Session.avatar(user, "avatar big"), mk("h2", "", user.username), wrap, dl, row);
}

input?.addEventListener("change", () => {
  const f = input.files[0];
  if (!f) return;
  // Downscale to 256px so it fits in localStorage.
  const img = new Image();
  img.onload = () => {
    const s = Math.min(1, 256 / Math.max(img.width, img.height));
    const c = document.createElement("canvas");
    c.width = img.width * s; c.height = img.height * s;
    c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
    Session.setPhoto(user, c.toDataURL("image/jpeg", 0.85));
    render();
  };
  img.src = URL.createObjectURL(f);
});

if (user) render();
