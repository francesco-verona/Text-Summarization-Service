const form = document.getElementById('form');
const text_cell = document.getElementById('text');
const statusEl = document.getElementById('status');
const result = document.getElementById('result');
const submitBtn = document.getElementById('submit');
// const clearBtn = document.getElementById('clear');
const wc = document.getElementById('wc');
const cc = document.getElementById('cc');

// Contatori rapidi
function updateKpis(){
    const words = text.value.trim().split(/\s+/).filter(Boolean).length;
    wc.textContent = words + (words === 1 ? ' parola' : ' parole');
    cc.textContent = text_cell.value.length + ' caratteri';
}
text.addEventListener('input', updateKpis);
updateKpis();

// clearBtn.addEventListener('click', () => {
//     text.value = '';
//     result.hidden = true;
//     result.textContent = '';
//     statusEl.textContent = '';
//     updateKpis();
//     text.focus();
// });

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        text: text.value.trim(),
        mode: document.getElementById('mode').value,
        // target: document.getElementById('target').value,
        // title: document.getElementById('title').value.trim() || null,
        // lang: document.getElementById('lang').value,
        // bullets: document.getElementById('bullets').value,
    };

    if(!payload.text){
        statusEl.textContent = 'Inserisci del testo da riassumere.';
        return;
    }

    // UI state
    submitBtn.disabled = true;
    statusEl.textContent = 'Sto generando il riassunto…';
    result.hidden = true;
    result.textContent = '';

    try {
        // 🔌 Modifica l'URL qui con il tuo endpoint backend
        const res = await fetch('http://127.0.0.1:5000/summarize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
    });

    if(!res.ok)
        throw new Error('Errore di rete (' + res.status + ')');

        // se tutto va a buon fine 
        const data = await res.json();
        
        result.textContent = data.summary || 'Nessun contenuto.';
        result.hidden = false;
        statusEl.textContent = 'Pronto.';
        } catch (err) {
            console.error(err);
            statusEl.innerHTML = '<span class="error">Errore: ' + (err.message || 'imprevisto') + '</span>';
        } finally {
            submitBtn.disabled = false;
        }
});