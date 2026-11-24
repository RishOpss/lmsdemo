// All requests go to a relative path; server.py proxies /api to the backend.
const API_URL = "/api/v1/users/";

const els = {
  body: document.getElementById("users-body"),
  table: document.getElementById("users-table"),
  status: document.getElementById("status"),
  search: document.getElementById("search"),
  role: document.getElementById("role"),
  count: document.getElementById("count"),
  refresh: document.getElementById("refresh"),
};

let users = [];
let sort = { key: "id", dir: "asc" };

function setStatus(msg, isError = false) {
  els.status.textContent = msg;
  els.status.classList.toggle("error", isError);
}

async function loadUsers() {
  els.refresh.disabled = true;
  els.table.hidden = true;
  setStatus("Loading users…");
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error(`Server responded ${res.status} ${res.statusText}`);
    users = await res.json();
    setStatus("");
    render();
  } catch (err) {
    setStatus(`Could not load users. ${err.message}`, true);
  } finally {
    els.refresh.disabled = false;
  }
}

function render() {
  const q = els.search.value.trim().toLowerCase();
  const role = els.role.value;
  const rows = users
    .filter((u) => (!role || u.role === role))
    .filter((u) => !q || [u.username, u.email, u.phone_number].some((v) => String(v ?? "").toLowerCase().includes(q)))
    .sort((a, b) => {
      const x = a[sort.key] ?? "", y = b[sort.key] ?? "";
      const c = typeof x === "number" ? x - y : String(x).localeCompare(String(y));
      return sort.dir === "asc" ? c : -c;
    });

  els.body.replaceChildren(...rows.map(rowEl));
  els.count.textContent = `${rows.length} of ${users.length} users`;
  els.table.hidden = rows.length === 0;
  if (rows.length === 0 && users.length) setStatus("No users match your filters.");
  else if (users.length === 0) setStatus("No users found.");
  else setStatus("");

  document.querySelectorAll("th").forEach((th) => {
    th.classList.remove("sorted-asc", "sorted-desc");
    if (th.dataset.key === sort.key) th.classList.add(`sorted-${sort.dir}`);
  });
}

function cell(text) {
  const td = document.createElement("td");
  td.textContent = text; // textContent avoids HTML injection
  return td;
}

function rowEl(u) {
  const tr = document.createElement("tr");
  tr.append(cell(u.id), cell(u.username), cell(u.email), cell(u.phone_number));
  const roleTd = document.createElement("td");
  const badge = document.createElement("span");
  badge.className = `badge ${u.role}`;
  badge.textContent = u.role;
  roleTd.append(badge);
  tr.append(roleTd, cell(new Date(u.created_at).toLocaleString()));
  return tr;
}

document.querySelectorAll("th").forEach((th) =>
  th.addEventListener("click", () => {
    const key = th.dataset.key;
    sort = { key, dir: sort.key === key && sort.dir === "asc" ? "desc" : "asc" };
    render();
  })
);
els.search.addEventListener("input", render);
els.role.addEventListener("change", render);
els.refresh.addEventListener("click", loadUsers);

loadUsers();
