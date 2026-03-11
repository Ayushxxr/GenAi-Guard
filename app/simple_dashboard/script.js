const API_BASE = "http://127.0.0.1:8000";

// --- Tab Switching Logic (Quick Launch) ---
function showScanner(scannerId) {
    // Hide all scanner cards
    document.querySelectorAll('.result-card').forEach(card => {
        card.classList.remove('active');
    });

    // Show selected scanner card
    const selectedCard = document.getElementById(scannerId + '-card');
    if (selectedCard) {
        selectedCard.classList.add('active');
        // Scroll to it
        selectedCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Update active state in sidebar/quick launch if needed
    // (Optional visual feedback)
}

// --- Helper: Status Badge Generator ---
function getStatusBadge(score, status) {
    const threshold = 50; // Default threshold
    if (status === "THREAT" || score > threshold) {
        return `<span class="badge badge-danger"><i class="fas fa-exclamation-triangle"></i> THREAT (${score})</span>`;
    }
    return `<span class="badge badge-safe"><i class="fas fa-check-circle"></i> SAFE (${score})</span>`;
}

function getAlertBadges(alerts) {
    if (!alerts || alerts.length === 0) return '';
    return alerts.map(a => `<div style="margin-top:5px; color:#ff7b72; font-size:0.8rem;">• ${a}</div>`).join('');
}

// --- API Interactions ---

// 1. Text Analysis
async function analyzeText() {
    const text = document.getElementById("textInput").value;
    const type = document.getElementById("textType").value;
    const resultBox = document.getElementById("textResult");

    if (!text) {
        resultBox.innerHTML = '<span style="color:var(--text-muted)">Please enter text to analyze.</span>';
        return;
    }

    resultBox.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Analyzing...';

    try {
        const res = await fetch(`${API_BASE}/api/v1/text/analyze`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text, check_type: type })
        });
        const data = await res.json();

        resultBox.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <strong>Result:</strong>
                ${getStatusBadge(data.risk_score, data.status)}
            </div>
            ${getAlertBadges(data.alerts)}
            <div style="margin-top:10px; font-size:0.8rem; color:var(--text-muted)">
                Analysis Complete.
            </div>
        `;
        fetchHistory(); // Refresh logs
    } catch (e) {
        resultBox.innerHTML = `<span style="color:var(--danger)">Error: ${e.message}</span>`;
    }
}

// 2. Web Scan
async function scanWeb() {
    const url = document.getElementById("urlInput").value;
    const resultBox = document.getElementById("webResult");

    if (!url) {
        resultBox.innerHTML = '<span style="color:var(--text-muted)">Please enter a URL.</span>';
        return;
    }

    resultBox.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Scanning URL...';

    try {
        const res = await fetch(`${API_BASE}/api/v1/web/scan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url, feature: "all" })
        });
        const data = await res.json();
        const isThreat = data.risk_score > 50;

        resultBox.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <strong>Verdict:</strong>
                ${getStatusBadge(data.risk_score, isThreat ? "THREAT" : "SAFE")}
            </div>
            ${getAlertBadges(data.alerts)}
        `;
        fetchHistory();
    } catch (e) {
        resultBox.innerHTML = `<span style="color:var(--danger)">Error: ${e.message}</span>`;
    }
}

// 3. File Scan
async function scanFile() {
    const fileInput = document.getElementById("fileInput");
    const resultBox = document.getElementById("fileResult");

    if (fileInput.files.length === 0) {
        resultBox.innerHTML = '<span style="color:var(--text-muted)">Please select a file.</span>';
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    resultBox.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Uploading & Scanning...';

    try {
        const res = await fetch(`${API_BASE}/api/v1/file/scan-file`, {
            method: "POST",
            body: formData
        });
        const data = await res.json();

        resultBox.innerHTML = `
             <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <strong>Verdict:</strong>
                ${getStatusBadge(data.risk_score, data.is_safe ? "SAFE" : "THREAT")}
            </div>
            ${getAlertBadges(data.alerts)}
        `;
        fetchHistory();
    } catch (e) {
        resultBox.innerHTML = `<span style="color:var(--danger)">Error: ${e.message}</span>`;
    }
}

// 4. Audio Scan
async function scanAudio() {
    const fileInput = document.getElementById("audioInput");
    const resultBox = document.getElementById("audioResult");

    if (fileInput.files.length === 0) {
        resultBox.innerHTML = '<span style="color:var(--text-muted)">Please select an audio file.</span>';
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    resultBox.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Analyzing Audio...';

    try {
        const res = await fetch(`${API_BASE}/api/v1/audio/detect-voice`, {
            method: "POST",
            body: formData
        });
        const data = await res.json();

        resultBox.innerHTML = `
             <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <strong>Verdict:</strong>
                ${getStatusBadge(data.risk_score, data.is_deepfake ? "THREAT" : "SAFE")}
            </div>
            ${getAlertBadges(data.alerts)}
            <div style="margin-top:5px; font-size:0.8rem;">Confidence: ${(data.confidence * 100).toFixed(1)}%</div>
        `;
        fetchHistory();
    } catch (e) {
        resultBox.innerHTML = `<span style="color:var(--danger)">Error: ${e.message}</span>`;
    }
}

// 5. Sandbox Audit
async function runSandboxAudit() {
    const resultBox = document.getElementById("sandboxResult");
    const targetUrl = document.getElementById("sandboxUrl").value;

    resultBox.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Running Security Audit... This may take a few seconds.';

    try {
        const res = await fetch(`${API_BASE}/api/v1/sandbox/scan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ target_url: targetUrl || null })
        });
        const data = await res.json();

        if (data.error) {
            resultBox.innerHTML = `<span style="color:var(--danger)">Error: ${data.error}</span>`;
            return;
        }

        const scoreColor = data.security_score < 70 ? 'var(--danger)' : 'var(--success)';

        resultBox.innerHTML = `
            <div style="margin-top: 15px; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 8px;">
                <h3 style="margin: 0 0 10px 0; color: ${scoreColor}">
                    Security Score: ${data.security_score}%
                </h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 10px;">
                    <div>Total: <strong>${data.total_tests}</strong></div>
                    <div style="color: var(--success)">Passed: <strong>${data.passed}</strong></div>
                    <div style="color: var(--danger)">Failed: <strong>${data.failed}</strong></div>
                </div>
                <div style="max-height: 200px; overflow-y: auto; font-size: 0.85rem; border-top: 1px solid var(--border-color); padding-top: 10px;">
                    ${data.details.map(d => `
                        <div style="margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.1);">
                            <div><strong>Prompt:</strong> ${d.prompt}</div>
                            <div style="color: ${d.status === 'SAFE' ? 'var(--success)' : 'var(--danger)'}">
                                <strong>${d.status}</strong> 
                                ${d.status === 'ERROR' ? `(${d.error})` : `(Risk: ${d.score})`}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    } catch (e) {
        resultBox.innerHTML = `<span style="color:var(--danger)">Connection Error: ${e.message}</span>`;
    }
}

// --- History & Stats ---

async function fetchHistory() {
    try {
        const res = await fetch(`${API_BASE}/api/v1/history`);
        const data = await res.json();
        updateStats(data);
        renderAlerts(data);
    } catch (e) {
        console.log("Error fetching history:", e);
    }
}

function updateStats(data) {
    // Calculate simple stats from the ephemeral log for demo purposes
    // specific counters will reset on server restart, but that's expected
    const totalScans = data.length;
    const threats = data.filter(item => item.status === 'THREAT').length;

    document.getElementById('stat-total-scans').innerText = totalScans;
    document.getElementById('stat-threats').innerText = threats;
}

function renderAlerts(data) {
    const container = document.getElementById('alertsList');
    if (data.length === 0) {
        container.innerHTML = '<div class="alert-item" style="text-align:center;">No recent alerts</div>';
        return;
    }

    // Show last 10
    const recent = data.slice().reverse().slice(0, 10);

    const html = recent.map(item => {
        const isThreat = item.status === 'THREAT';
        const color = isThreat ? 'var(--danger)' : 'var(--success)';
        const icon = isThreat ? 'exclamation-triangle' : 'check-circle';

        return `
        <div class="alert-item" style="border-left: 3px solid ${color}">
            <div class="alert-header">
                <span class="alert-module" style="color:${color}">${item.module}</span>
                <span class="alert-time">${item.timestamp.split(' ')[1]}</span>
            </div>
            <div style="font-size:0.9rem; margin-top:4px;">
                ${item.input_type || 'Scan Request'}
            </div>
            ${item.alerts.length > 0 ? `<div style="color:var(--text-muted); font-size:0.8rem; margin-top:4px;">${item.alerts[0]}</div>` : ''}
        </div>
        `;
    }).join('');

    container.innerHTML = html;
}

// Init
document.addEventListener('DOMContentLoaded', () => {
    fetchHistory();
    setInterval(fetchHistory, 3000);

    // Default show Text scanner
    showScanner('text');
});
