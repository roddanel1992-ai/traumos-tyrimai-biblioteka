// Gauti straipsnio ID iš URL
function getStraipsnioId() {
    const urlParams = new URLSearchParams(window.location.search);
    return parseInt(urlParams.get('id'));
}

// Užkrauti konkretų straipsnį
function loadStraipsnis() {
    const id = getStraipsnioId();

    if (!id) {
        window.location.href = 'index.html';
        return;
    }

    const straipsnis = straipsniuDuomenys.find(s => s.id === id);

    if (straipsnis) {
        displayStraipsnis(straipsnis);
    } else {
        document.getElementById('straipsnis-container').innerHTML =
            '<p>Straipsnis nerastas.</p>';
    }
}

// Rodyti straipsnio turinį
function displayStraipsnis(straipsnis) {
    const container = document.getElementById('straipsnis-container');

    // Raktiniai žodžiai
    const keywords = straipsnis.raktiniai_zodziai
        .map(zodis => `<span class="keyword-tag">${zodis}</span>`)
        .join('');

    // Turinys
    const turinys = straipsnis.turinys;
    let turinyHTML = '';

    for (const [key, value] of Object.entries(turinys)) {
        const pavadinimas = formatSectionTitle(key);
        turinyHTML += `
            <h2>${pavadinimas}</h2>
            <p>${value}</p>
        `;
    }

    container.innerHTML = `
        <article class="straipsnio-turinys">
            <h1>${straipsnis.pavadinimas}</h1>

            <div class="meta-info">
                <p><strong>Autoriai:</strong> ${straipsnis.autoriai}</p>
                <p><strong>Institucija:</strong> ${straipsnis.institucija}</p>
                <p><strong>Metai:</strong> ${straipsnis.metai}</p>
                <p><strong>Šaltinis:</strong> ${straipsnis.saltinis}</p>
                ${straipsnis.doi ? `<p><strong>DOI:</strong> <a href="${straipsnis.doi}" target="_blank">${straipsnis.doi}</a></p>` : ''}
                ${straipsnis.pdf_file ? `<p><strong>PDF:</strong> <a href="${straipsnis.pdf_file}" target="_blank" rel="noopener noreferrer">Atidaryti originalų PDF</a></p>` : ''}
                ${straipsnis.pilnas_vertimas ? `<p><strong>Pilnas vertimas:</strong> <a href="${straipsnis.pilnas_vertimas}">Skaityti pilną lietuvišką vertimą</a></p>` : ''}
            </div>

            <h2>Santrauka</h2>
            <p>${straipsnis.santrauka}</p>

            <div class="raktiniai-zodziai">
                <strong>Raktiniai žodžiai:</strong>
                ${keywords}
            </div>

            ${turinyHTML}
        </article>
    `;
}

// Formatuoti skyriaus pavadinimą
function formatSectionTitle(key) {
    const titles = {
        'ivadinė_dalis': 'Įvadinė dalis',
        'trauminio_streso_tyrimu_kilimas': 'Trauminio streso tyrimų kilimas Baltijos valstybėse',
        'politinio_smurto_tyrimai': 'Politinio smurto tyrimai',
        'traumos_ir_ptss_paplitimas': 'Traumos ir PTSS paplitimas',
        'nelaimes_tyrimai': 'Nelaimių tyrimai',
        'raidos_perspektyva': 'Raidos perspektyva',
        'ateities_kryptys': 'Ateities kryptys trauma tyrimams ir praktikai Baltijos valstybėse'
    };

    return titles[key] || key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Inicializuoti puslapį
document.addEventListener('DOMContentLoaded', () => {
    loadStraipsnis();
});
