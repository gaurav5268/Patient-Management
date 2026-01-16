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
    const input = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");

    const question = input.value.trim();
    if (!question) return;

    chatBox.innerHTML = `<p class="hint">Thinking...</p>`;

    const response = await fetch("/chat-db", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
    });

    const data = await response.json();
    console.log(data);  // keep this for now

    // Clean layout
    let html = `
        <div class="message">
            <div class="bubble user"><strong>You:</strong> ${data.question}</div>
            <div class="bubble ai"><strong>AI:</strong> ${data.response_text}</div>
        </div>
    `;

    // Always use rows only for table
    if (Array.isArray(data.rows) && data.rows.length > 0) {
        html += createTable(data.rows);
    }

    chatBox.innerHTML = html;
    input.value = "";
}


function createTable(rows) {
    const columns = Object.keys(rows[0]);

    let table = `
        <div class="table-container">
            <table class="result-table">
                <thead>
                    <tr>
                        ${columns.map(col => `<th>${col}</th>`).join("")}
                    </tr>
                </thead>
                <tbody>
    `;

    rows.forEach(row => {
        table += `
            <tr>
                ${columns.map(col => `<td>${row[col]}</td>`).join("")}
            </tr>
        `;
    });

    table += `
                </tbody>
            </table>
        </div>
    `;

    return table;
}
