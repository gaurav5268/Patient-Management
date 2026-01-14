const API = "http://127.0.0.1:8000";

async function submitPatient() {
  const form = document.getElementById("addForm");
  const data = Object.fromEntries(new FormData(form));

  data.age = Number(data.age);
  data.height = Number(data.height);
  data.weight = Number(data.weight);
  data.symptoms = data.symptoms.split(",").map(s => s.trim());

  const res = await fetch(`${API}/patients`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  });

  document.getElementById("result").textContent = await res.text();
}

async function loadPatient() {
  const id = document.getElementById("pid").value;
  const res = await fetch(`${API}/patients/${id}`);
  const data = await res.json();

  updateForm.style.display = "block";
  name.value = data.name;
  city.value = data.city;
}

async function updatePatient() {
  const id = pid.value;

  const payload = {
    name: name.value,
    city: city.value
  };

  const res = await fetch(`${API}/patients/${id}`, {
    method: "PUT",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  });

  document.getElementById("result").textContent = await res.text();
}

async function viewPatient() {
  const id = document.getElementById("vid").value;
  window.location.href = `/profile/${id}`;
}


async function predictDisease(symptomsStr) {
  const symptoms = symptomsStr.split(",").map(s => s.trim());

  const res = await fetch("http://127.0.0.1:8000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ symptoms })
  });

  const data = await res.json();

  document.getElementById("prediction").textContent =
    "Predicted Disease: " + data.predicted_disease +
    "\nConfidence: " + data.confidence + "%";
}

async function sendQuery() {
  const input = document.getElementById("userInput").value;
  if (!input) return;

  const chat = document.getElementById("chatBox");
  chat.innerHTML += `<p><b>You:</b> ${input}</p>`;

  const res = await fetch("/chat-db", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: input })
  });

  const data = await res.json();

  chat.innerHTML += `<p><b>AI:</b> ${data.response_text}</p>`;

  if (data.rows.length > 0) {
    chat.innerHTML += `<pre>${JSON.stringify(data.rows, null, 2)}</pre>`;
  }

  document.getElementById("userInput").value = "";
}
