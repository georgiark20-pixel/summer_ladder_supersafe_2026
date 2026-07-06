let currentUser = null;

// STORAGE
function getUsers() {
  return JSON.parse(localStorage.getItem("users")) || {};
}

function saveUsers(users) {
  localStorage.setItem("users", JSON.stringify(users));
}

// AUTH
function signup() {
  let users = getUsers();

  let id = document.getElementById("userId").value;
  let name = document.getElementById("name").value;

  if (!id || !name) return alert("Fill all fields");

  if (users[id]) return alert("User exists");

  users[id] = {
    name,
    friends: [],
    theme: "dark",
    logs: []
  };

  saveUsers(users);
  alert("Account created!");
}

function login() {
  let users = getUsers();
  let id = document.getElementById("userId").value;

  if (!users[id]) return alert("User not found");

  currentUser = id;

  document.getElementById("loginView").classList.add("hidden");
  document.getElementById("appView").classList.remove("hidden");

  document.getElementById("welcome").innerText =
    "Welcome " + users[id].name;

  document.getElementById("uid").innerText =
    "User ID: " + id;

  renderFriends();
  renderLogs();
  applyTheme();
}

function logout() {
  location.reload();
}

// ENCRYPTION
function encrypt() {
  let users = getUsers();
  let text = document.getElementById("input").value;
  let algo = document.getElementById("algo").value;

  let status = document.getElementById("status");
  status.innerText = "Encrypting...";

  setTimeout(() => {

    let encoded = btoa(text.split("").reverse().join(""));

    document.getElementById("output").innerText =
      "Encrypted: " + encoded;

    document.getElementById("key").innerText =
      "Key: " + Math.random().toString(36).substring(2, 10);

    status.innerText = "Complete";

    addLog(`Encrypted using ${algo}`);
  }, 1000);
}

// FRIENDS
function addFriend() {
  let users = getUsers();

  let fid = document.getElementById("friendInput").value;

  if (!users[fid]) return alert("User not found");

  users[currentUser].friends.push(fid);

  saveUsers(users);

  addLog("Added friend " + fid);
  renderFriends();
}

function renderFriends() {
  let users = getUsers();
  let list = users[currentUser].friends;

  document.getElementById("friends").innerHTML =
    list.map(f => `<div>👤 ${f}</div>`).join("");
}

// LOGS
function addLog(msg) {
  let users = getUsers();

  users[currentUser].logs.push(msg);

  saveUsers(users);

  renderLogs();
}

function renderLogs() {
  let users = getUsers();

  document.getElementById("logs").innerHTML =
    (users[currentUser].logs || [])
    .slice(-10)
    .map(l => `<div>${l}</div>`)
    .join("");
}

// THEMES
function setTheme(theme) {
  let users = getUsers();
  users[currentUser].theme = theme;
  saveUsers(users);
  applyTheme();
}

function applyTheme() {
  let users = getUsers();
  document.body.className = users[currentUser].theme;
}