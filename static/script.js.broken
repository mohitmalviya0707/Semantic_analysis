(() => {
  "use strict";

<<<<<<< Updated upstream
  // Render FastAPI backend
  const API_URL = "https://semantic-analysis-api.onrender.com";

=======
>>>>>>> Stashed changes
  const EMOJI = {
    sadness: "😢",
    joy: "😄",
    love: "❤️",
    anger: "😠",
    fear: "😨",
    surprise: "😲",
  };

  const el = {
    statusDot: document.getElementById("statusDot"),
    serverStatusText: document.getElementById("serverStatusText"),
    textInput: document.getElementById("textInput"),
    charCount: document.getElementById("charCount"),
    analyzeBtn: document.getElementById("analyzeBtn"),
    errorMsg: document.getElementById("errorMsg"),
    orb: document.getElementById("orb"),
    orbEmoji: document.getElementById("orbEmoji"),
    resultSection: document.getElementById("resultSection"),
    emotionWord: document.getElementById("emotionWord"),
    emotionEmoji: document.getElementById("emotionEmoji"),
    confidenceText: document.getElementById("confidenceText"),
    echoedText: document.getElementById("echoedText"),
    barsContainer: document.getElementById("barsContainer"),
  };

  let modelReady = false;

<<<<<<< Updated upstream
  async function checkHealth() {
    try {
      // Render backend
      const res = await fetch(`${API_URL}/health`);

      if (!res.ok) throw new Error("bad status");

      const data = await res.json();

      modelReady = !!data.model_loaded;

=======
  /* ---------------------------------------------------------------
     Health check — poll until the model is loaded
  --------------------------------------------------------------- */
  async function checkHealth() {
    try {
      const res = await fetch("/health");
      if (!res.ok) throw new Error("bad status");
      const data = await res.json();

      modelReady = !!data.model_loaded;
>>>>>>> Stashed changes
      if (modelReady) {
        setStatus("live", "model ready — say something");
      } else {
        setStatus("warming", "waking the model up…");
        setTimeout(checkHealth, 3000);
      }
    } catch (e) {
<<<<<<< Updated upstream
      console.error("Health check failed:", e);
      setStatus("down", "can't reach the server");
      setTimeout(checkHealth, 5000);
    }

=======
      setStatus("down", "can't reach the server");
      setTimeout(checkHealth, 5000);
    }
>>>>>>> Stashed changes
    syncButtonState();
  }

  function setStatus(kind, text) {
    el.statusDot.className = "brand-mark " + kind;
    el.serverStatusText.textContent = text;
  }

<<<<<<< Updated upstream
=======
  /* ---------------------------------------------------------------
     Input handling
  --------------------------------------------------------------- */
>>>>>>> Stashed changes
  el.textInput.addEventListener("input", () => {
    el.charCount.textContent = el.textInput.value.length;
    syncButtonState();
  });

  el.textInput.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      runAnalysis();
    }
  });

  function syncButtonState() {
    const hasText = el.textInput.value.trim().length > 0;
    el.analyzeBtn.disabled = !hasText || !modelReady;
  }

  el.analyzeBtn.addEventListener("click", runAnalysis);

<<<<<<< Updated upstream
  async function runAnalysis() {
    const text = el.textInput.value.trim();

=======
  /* ---------------------------------------------------------------
     Analysis flow
  --------------------------------------------------------------- */
  async function runAnalysis() {
    const text = el.textInput.value.trim();
>>>>>>> Stashed changes
    if (!text || !modelReady) return;

    hideError();
    enterThinking();

    try {
<<<<<<< Updated upstream
      // Render backend
      const res = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
=======
      const res = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
>>>>>>> Stashed changes
        body: JSON.stringify({ text }),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
        const detail =
          body && body.detail
            ? typeof body.detail === "string"
              ? body.detail
              : "The model couldn't process that sentence."
            : `Request failed (${res.status}).`;
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
        throw new Error(detail);
      }

      const data = await res.json();
<<<<<<< Updated upstream

      renderResult(data, text);

    } catch (err) {
      console.error("Prediction failed:", err);
=======
      renderResult(data, text);
    } catch (err) {
>>>>>>> Stashed changes
      exitThinking(false);
      showError(err.message || "Something went wrong. Try again.");
    }
  }

  function enterThinking() {
    el.analyzeBtn.classList.add("loading");
    el.analyzeBtn.querySelector(".btn-label").textContent = "Reading…";
    el.analyzeBtn.disabled = true;
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
    el.orb.classList.remove("settled");
    el.orb.classList.add("thinking");
    el.orbEmoji.style.opacity = "0";
  }

  function exitThinking(success) {
    el.analyzeBtn.classList.remove("loading");
    el.analyzeBtn.querySelector(".btn-label").textContent = "Read the mood";
<<<<<<< Updated upstream

    syncButtonState();

    el.orb.classList.remove("thinking");

=======
    syncButtonState();
    el.orb.classList.remove("thinking");
>>>>>>> Stashed changes
    if (!success) {
      el.orbEmoji.textContent = "✎";
      el.orbEmoji.style.opacity = "1";
    }
  }

  function renderResult(data, originalText) {
    const emotion = data.predicted_emotion;
    const emoji = EMOJI[emotion] || "🙂";

    document.body.setAttribute("data-emotion", emotion);

    el.orb.classList.add("settled");
    el.orbEmoji.textContent = emoji;
    el.orbEmoji.style.opacity = "1";
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
    exitThinking(true);

    el.emotionWord.textContent = capitalize(emotion);
    el.emotionEmoji.textContent = emoji;
<<<<<<< Updated upstream

    el.confidenceText.textContent =
      `${(data.confidence * 100).toFixed(1)}% confidence`;

=======
    el.confidenceText.textContent = `${(data.confidence * 100).toFixed(1)}% confidence`;
>>>>>>> Stashed changes
    el.echoedText.textContent = `“${originalText}”`;

    renderBars(data.all_probabilites);

    el.resultSection.hidden = false;
    el.resultSection.classList.remove("entering");
<<<<<<< Updated upstream

    void el.resultSection.offsetWidth;

    el.resultSection.classList.add("entering");

    el.resultSection.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
    });
  }

  function renderBars(probs) {
    const entries = Object.entries(probs)
      .sort((a, b) => b[1] - a[1]);

=======
    void el.resultSection.offsetWidth; // restart animation
    el.resultSection.classList.add("entering");

    el.resultSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function renderBars(probs) {
    const entries = Object.entries(probs).sort((a, b) => b[1] - a[1]);
>>>>>>> Stashed changes
    el.barsContainer.innerHTML = "";

    entries.forEach(([label, value], i) => {
      const pct = value * 100;
<<<<<<< Updated upstream

      const row = document.createElement("div");

      row.className = `bar-row bar-${label}`;

      row.innerHTML = `
        <span class="bar-label">
          ${EMOJI[label] || ""} ${label}
        </span>

        <span class="bar-track">
          <span class="bar-fill"></span>
        </span>

        <span class="bar-pct">
          ${pct.toFixed(1)}%
        </span>
      `;

      el.barsContainer.appendChild(row);

      const fill = row.querySelector(".bar-fill");

=======
      const row = document.createElement("div");
      row.className = `bar-row bar-${label}`;
      row.innerHTML = `
        <span class="bar-label">${EMOJI[label] || ""} ${label}</span>
        <span class="bar-track"><span class="bar-fill"></span></span>
        <span class="bar-pct">${pct.toFixed(1)}%</span>
      `;
      el.barsContainer.appendChild(row);

      const fill = row.querySelector(".bar-fill");
>>>>>>> Stashed changes
      setTimeout(() => {
        fill.style.width = pct + "%";
      }, 60 + i * 70);
    });
  }

  function showError(msg) {
    el.errorMsg.textContent = msg;
    el.errorMsg.hidden = false;
  }
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
  function hideError() {
    el.errorMsg.hidden = true;
  }

  function capitalize(s) {
    return s.charAt(0).toUpperCase() + s.slice(1);
  }

<<<<<<< Updated upstream
  // Start health check
  checkHealth();

})();
=======
  /* ---------------------------------------------------------------
     Boot
  --------------------------------------------------------------- */
  checkHealth();
})();
>>>>>>> Stashed changes
