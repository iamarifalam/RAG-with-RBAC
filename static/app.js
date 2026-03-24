const state = {
  token: null,
  role: null,
};

const authStatus = document.querySelector("#auth-status");
const answer = document.querySelector("#answer");
const reason = document.querySelector("#reason");
const responsePanel = document.querySelector("#response-panel");
const sources = document.querySelector("#sources");

document.querySelectorAll(".demo-user").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelector("#username").value = button.dataset.username;
    document.querySelector("#password").value = button.dataset.password;
  });
});

document.querySelector("#login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const username = document.querySelector("#username").value;
  const password = document.querySelector("#password").value;

  const response = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await response.json();
  if (!response.ok) {
    authStatus.textContent = data.detail || "Login failed";
    return;
  }

  state.token = data.access_token;
  state.role = data.role;
  authStatus.textContent = `Signed in as ${data.display_name} (${data.role})`;
});

document.querySelector("#chat-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!state.token) {
    authStatus.textContent = "Sign in first.";
    return;
  }

  const question = document.querySelector("#question").value;
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${state.token}`,
    },
    body: JSON.stringify({ question }),
  });
  const data = await response.json();
  responsePanel.classList.remove("hidden");
  answer.textContent = data.answer;
  reason.textContent = data.reason ? `Reason: ${data.reason}` : `Trace ID: ${data.trace_id}`;
  sources.innerHTML = "";
  (data.sources || []).forEach((source) => {
    const item = document.createElement("li");
    item.textContent = `${source.title} (${source.topic}) score=${source.score}`;
    sources.appendChild(item);
  });
});

document.querySelector("#reindex-button").addEventListener("click", async () => {
  if (!state.token) {
    authStatus.textContent = "Sign in first.";
    return;
  }
  const response = await fetch("/api/admin/reindex", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${state.token}`,
    },
  });
  const data = await response.json();
  authStatus.textContent = response.ok
    ? `Reindex completed: ${data.chunks} chunks`
    : data.detail || "Reindex failed";
});

