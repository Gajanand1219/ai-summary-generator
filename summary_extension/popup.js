document.addEventListener("DOMContentLoaded", async () => {
  const summaryBox = document.getElementById("summary");
  const player = document.getElementById("player");

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const url = tab.url;
    console.log("Detected URL:", url);  // Debug log

    // ✅ Handle PDF-like URLs (arXiv and others)
    if (url.includes("/pdf/") || url.endsWith(".pdf")) {
      summaryBox.textContent = "📄 Reading PDF from link...";

      const res = await fetch("http://localhost:8000/api/summary-from-pdf-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pdf_url: url })
      });

      if (!res.ok) throw new Error("Failed to get PDF summary.");
      const data = await res.json();
      summaryBox.textContent = data.summary;

      const audioRes = await fetch("http://localhost:8000/api/speak-line", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: data.summary, language: "en" })
      });

      const blob = await audioRes.blob();
      player.src = URL.createObjectURL(blob);
      player.hidden = false;
      player.load();
      player.play();
      return;
    }

    // ✅ Handle normal web page
    const [{ result: pageText }] = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => document.body.innerText
    });

    if (!pageText || pageText.trim().length === 0) {
      summaryBox.textContent = "❌ Couldn't extract readable content from this page.";
      return;
    }

    summaryBox.textContent = "⏳ Summarizing web page...";

    const res = await fetch("http://localhost:8000/api/summary-from-text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: pageText })
    });

    const data = await res.json();
    summaryBox.textContent = data.summary;

    const audioRes = await fetch("http://localhost:8000/api/speak-line", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: data.summary, language: "en" })
    });

    const blob = await audioRes.blob();
    player.src = URL.createObjectURL(blob);
    player.hidden = false;
    player.load();
    player.play();

  } catch (err) {
    console.error(err);
    summaryBox.textContent = "❌ Failed to summarize.";
    player.hidden = true;
  }
});
