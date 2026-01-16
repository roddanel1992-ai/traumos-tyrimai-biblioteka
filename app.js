// Užkrauti straipsnius
function loadStraipsniai() {
    displayStraipsniai(straipsniuDuomenys);
}

// Rodyti straipsnius puslapyje
function displayStraipsniai(straipsniai) {
    const container = document.getElementById('straipsniai-container');
    container.innerHTML = '';

    straipsniai.forEach(straipsnis => {
        const card = createStraipsnioCard(straipsnis);
        container.appendChild(card);
    });
}

// Sukurti straipsnio kortelę
function createStraipsnioCard(straipsnis) {
    const card = document.createElement('div');
    card.className = 'straipsnis-card';

    // Raktiniai žodžiai
    const keywords = straipsnis.raktiniai_zodziai
        .map(zodis => `<span class="keyword-tag">${zodis}</span>`)
        .join('');

    card.innerHTML = `
        <h3>${straipsnis.pavadinimas}</h3>
        <p class="autoriai">${straipsnis.autoriai}</p>
        <p class="metai">${straipsnis.metai} m.</p>
        <p class="santrauka">${straipsnis.santrauka}</p>
        <div class="raktiniai-zodziai">
            ${keywords}
        </div>
        <a href="straipsnis.html?id=${straipsnis.id}" class="skaityti-btn">Skaityti daugiau</a>
    `;

    return card;
}

// Inicializuoti puslapį
document.addEventListener('DOMContentLoaded', () => {
    loadStraipsniai();
});
