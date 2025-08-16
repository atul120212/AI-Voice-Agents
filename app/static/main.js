function showLoading(targetId) {
  document.getElementById(targetId).innerHTML = "<em>⏳ Processing...</em>";
}

document.getElementById("llmForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  showLoading("llmResponse");
  let text = document.getElementById("llmText").value;
  let res = await fetch("/llm/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  let data = await res.json();
  document.getElementById("llmResponse").innerText =
    data.response || data.error;
});

document.getElementById("uploadForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  showLoading("uploadResult");
  let formData = new FormData(e.target);
  let res = await fetch("/upload", { method: "POST", body: formData });
  let data = await res.json();
  document.getElementById("uploadResult").innerText = JSON.stringify(
    data,
    null,
    2
  );
});

document
  .getElementById("transcribeForm")
  ?.addEventListener("submit", async (e) => {
    e.preventDefault();
    showLoading("transcribeResult");
    let formData = new FormData(e.target);
    let res = await fetch("/transcribe/file", {
      method: "POST",
      body: formData,
    });
    let data = await res.json();
    document.getElementById("transcribeResult").innerText =
      data.transcription || data.error;
  });

document.getElementById("ttsForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  showLoading("ttsResult");
  let formData = new FormData(e.target);
  let res = await fetch("/tts/echo", { method: "POST", body: formData });
  let data = await res.json();
  document.getElementById("ttsResult").innerHTML = `
        <p><b>Transcription:</b> ${data.transcription}</p>
        <audio controls src="${data.murf_audio_url}"></audio>
    `;
});
