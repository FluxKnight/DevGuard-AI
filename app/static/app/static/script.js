const API_BASE = window.location.origin;

    const els = {
      filename: document.getElementById("filenameInput"),
      language: document.getElementById("languageInput"),
      code: document.getElementById("codeInput"),
      file: document.getElementById("fileInput"),
      scan: document.getElementById("scanBtn"),
      clear: document.getElementById("clearBtn"),
      loadSample: document.getElementById("loadSampleBtn"),
      history: document.getElementById("historyBtn"),
      markdown: document.getElementById("markdownBtn"),
      emptyState: document.getElementById("emptyState"),
      resultContent: document.getElementById("resultContent"),
      reviewId: document.getElementById("reviewIdBadge"),
      riskLevel: document.getElementById("riskLevel"),
      scoreValue: document.getElementById("scoreValue"),
      summary: document.getElementById("summaryText"),
      findings: document.getElementById("findingsList"),
      historyList: document.getElementById("historyList"),
      heroScore: document.getElementById("heroScore"),
      heroRiskText: document.getElementById("heroRiskText"),
      scrollToScanner: document.getElementById("scrollToScanner")
    };

    let currentReviewId = null;

    const sampleCode = `password = "admin123"
api_key = "sk_test_123456789"
query = "SELECT * FROM users WHERE name = " + username
debug = True

import os
import hashlib

os.system("ping " + host)
hashlib.md5(b"test")`;

    function escapeHtml(value) {
      return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    function detectLanguage(filename) {
      const ext = filename.split(".").pop()?.toLowerCase();
      const map = {
        py: "python",
        js: "javascript",
        ts: "typescript",
        cpp: "cpp",
        c: "cpp",
        h: "cpp",
        hpp: "cpp",
        java: "java",
        php: "php",
        go: "go",
        rs: "rust",
        env: "unknown",
        txt: "unknown"
      };
      return map[ext] || "unknown";
    }

    function setLoading(isLoading) {
      els.scan.disabled = isLoading;
      els.scan.textContent = isLoading ? "Analyzing..." : "Analyze Code";
    }

    function riskClass(level) {
      return String(level || "LOW").toUpperCase();
    }

    function renderResult(data) {
      currentReviewId = data.review_id;
      els.emptyState.classList.add("hidden");
      els.resultContent.classList.remove("hidden");

      els.reviewId.textContent = data.review_id ? `Review #${data.review_id}` : "Unsaved review";
      els.riskLevel.textContent = data.risk_level;
      els.scoreValue.textContent = data.score;
      els.heroScore.textContent = data.score;
      els.heroRiskText.textContent = `${data.risk_level} risk detected`;
      els.summary.textContent = data.summary;

      const findings = data.findings || [];

      if (findings.length === 0) {
        els.findings.innerHTML = `<div class="finding"><h5>No findings detected</h5><p>The current MVP rule set did not detect obvious security risks.</p></div>`;
        return;
      }

      els.findings.innerHTML = findings.map((finding) => {
        const sev = riskClass(finding.severity);
        return `
          <article class="finding">
            <div class="finding-top">
              <h5>${escapeHtml(finding.title)}</h5>
              <span class="severity ${sev}">${escapeHtml(sev)}</span>
            </div>
            <div class="finding-meta">
              Category: ${escapeHtml(finding.category)} · Line: ${escapeHtml(finding.line ?? "N/A")}
            </div>
            <p><strong>Explanation:</strong> ${escapeHtml(finding.explanation)}</p>
            <p><strong>Fix:</strong> ${escapeHtml(finding.recommendation)}</p>
            ${finding.matched_text ? `<div class="matched">${escapeHtml(finding.matched_text)}</div>` : ""}
          </article>
        `;
      }).join("");
    }

    async function scanCode() {
      const filename = els.filename.value.trim() || "untitled.txt";
      const language = els.language.value;
      const code = els.code.value;

      if (!code.trim()) {
        alert("Paste code or upload a file first.");
        return;
      }

      setLoading(true);

      try {
        const res = await fetch(`${API_BASE}/api/v1/reviews`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ filename, language, code })
        });

        if (!res.ok) {
          const text = await res.text();
          throw new Error(text);
        }

        const data = await res.json();
        renderResult(data);
        loadHistory();
      } catch (err) {
        alert(`Scan failed: ${err.message}`);
      } finally {
        setLoading(false);
      }
    }

    async function loadHistory() {
      try {
        const res = await fetch(`${API_BASE}/api/v1/reviews`);
        if (!res.ok) throw new Error(await res.text());

        const reviews = await res.json();

        if (!reviews.length) {
          els.historyList.innerHTML = `<p class="muted">No reviews stored yet.</p>`;
          return;
        }

        els.historyList.innerHTML = reviews.slice(0, 8).map((item) => `
          <div class="history-item">
            <div>
              <strong>${escapeHtml(item.filename)}</strong>
              <span>${escapeHtml(item.language)} · ${escapeHtml(item.summary)}</span>
            </div>
            <span class="severity ${riskClass(item.risk_level)}">${escapeHtml(item.risk_level)} · ${escapeHtml(item.score)}/100</span>
          </div>
        `).join("");
      } catch (err) {
        els.historyList.innerHTML = `<p class="muted">Could not load history: ${escapeHtml(err.message)}</p>`;
      }
    }

    function openMarkdownReport() {
      if (!currentReviewId) {
        alert("Run a scan first.");
        return;
      }
      window.open(`${API_BASE}/api/v1/reports/${currentReviewId}/markdown`, "_blank");
    }

    els.scan.addEventListener("click", scanCode);
    els.history.addEventListener("click", loadHistory);
    els.markdown.addEventListener("click", openMarkdownReport);

    els.clear.addEventListener("click", () => {
      els.code.value = "";
      els.filename.value = "login.py";
      els.language.value = "python";
      currentReviewId = null;
      els.emptyState.classList.remove("hidden");
      els.resultContent.classList.add("hidden");
      els.reviewId.textContent = "No review yet";
      els.heroScore.textContent = "0";
      els.heroRiskText.textContent = "Waiting for scan";
    });

    els.loadSample.addEventListener("click", () => {
      els.filename.value = "login.py";
      els.language.value = "python";
      els.code.value = sampleCode;
      document.getElementById("scanner").scrollIntoView({ behavior: "smooth" });
    });

    els.scrollToScanner.addEventListener("click", () => {
      document.getElementById("scanner").scrollIntoView({ behavior: "smooth" });
    });

    els.file.addEventListener("change", async (event) => {
      const file = event.target.files?.[0];
      if (!file) return;

      els.filename.value = file.name;
      els.language.value = detectLanguage(file.name);
      els.code.value = await file.text();
    });

    loadHistory();
