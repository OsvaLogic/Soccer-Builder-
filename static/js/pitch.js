// Archivo: static/js/pitch.js
// Etiqueta: Lógica de UI para la pizarra y guardado de formaciones

document.addEventListener('DOMContentLoaded', () => {
    
    // --- SISTEMA DE NOTIFICACIONES TOAST ---
    function showToast(message, type="success") {
        let toast = document.getElementById("toast-notification");
        if (!toast) {
            toast = document.createElement("div");
            toast.id = "toast-notification";
            document.body.appendChild(toast);
        }
        toast.className = `toast show ${type}`;
        toast.innerText = message;
        setTimeout(() => { toast.classList.remove("show"); }, 3000);
    }

    // --- CALCULADOR DE RAREZAS VISUALES ---
    function updateCardRarity(card, rating) {
        card.classList.remove('card-bronze', 'card-silver', 'card-gold', 'card-special');
        if (rating < 65) card.classList.add('card-bronze'); else if (rating < 75) card.classList.add('card-silver'); else if (rating < 90) card.classList.add('card-gold'); else card.classList.add('card-special');
    }

    const formationSelect = document.getElementById('formation-select');
    const saveBtn = document.getElementById('save-team-btn');

    // --- COORDENADAS TÁCTICAS (X%, Y%) ---
    // El Portero (GK) siempre es el índice 0, luego Defensas, Medios y Delanteros
    const tacticalCoords = {
        '4-4-2': [
            {x: 50, y: 90}, // PORTERO
            {x: 20, y: 75}, {x: 40, y: 80}, {x: 60, y: 80}, {x: 80, y: 75}, // DEFENSAS
            {x: 20, y: 50}, {x: 40, y: 50}, {x: 60, y: 50}, {x: 80, y: 50}, // MEDIOS
            {x: 40, y: 20}, {x: 60, y: 20} // DELANTEROS
        ],
        '4-3-3': [
            {x: 50, y: 90},
            {x: 20, y: 75}, {x: 40, y: 80}, {x: 60, y: 80}, {x: 80, y: 75},
            {x: 50, y: 65}, {x: 30, y: 50}, {x: 70, y: 50},
            {x: 20, y: 25}, {x: 50, y: 15}, {x: 80, y: 25}
        ],
        '4-2-3-1': [
            {x: 50, y: 90},
            {x: 20, y: 75}, {x: 40, y: 80}, {x: 60, y: 80}, {x: 80, y: 75},
            {x: 35, y: 60}, {x: 65, y: 60},
            {x: 20, y: 35}, {x: 50, y: 35}, {x: 80, y: 35},
            {x: 50, y: 15}
        ],
        '5-3-2': [
            {x: 50, y: 90},
            {x: 15, y: 70}, {x: 30, y: 80}, {x: 50, y: 80}, {x: 70, y: 80}, {x: 85, y: 70},
            {x: 30, y: 50}, {x: 50, y: 55}, {x: 70, y: 50},
            {x: 35, y: 20}, {x: 65, y: 20}
        ],
        '5-4-1': [
            {x: 50, y: 90},
            {x: 15, y: 70}, {x: 30, y: 80}, {x: 50, y: 80}, {x: 70, y: 80}, {x: 85, y: 70},
            {x: 20, y: 45}, {x: 40, y: 50}, {x: 60, y: 50}, {x: 80, y: 45},
            {x: 50, y: 15}
        ],
        '3-2-4-1': [
            {x: 50, y: 90},
            {x: 30, y: 80}, {x: 50, y: 80}, {x: 70, y: 80},
            {x: 35, y: 60}, {x: 65, y: 60},
            {x: 15, y: 40}, {x: 35, y: 35}, {x: 65, y: 35}, {x: 85, y: 40},
            {x: 50, y: 15}
        ],
        '3-4-3': [
            {x: 50, y: 90},
            {x: 30, y: 80}, {x: 50, y: 80}, {x: 70, y: 80},
            {x: 15, y: 50}, {x: 40, y: 55}, {x: 60, y: 55}, {x: 85, y: 50},
            {x: 25, y: 20}, {x: 50, y: 15}, {x: 75, y: 20}
        ]
    };

    if (formationSelect) {
        formationSelect.addEventListener('change', (e) => {
            const formation = e.target.value;
            if (formation && tacticalCoords[formation]) {
                const coords = tacticalCoords[formation];
                document.querySelectorAll('.player-node').forEach((player, index) => {
                    if (coords[index]) {
                        // Añadir transición suave para el movimiento
                        player.style.transition = 'top 0.6s cubic-bezier(0.25, 0.8, 0.25, 1), left 0.6s cubic-bezier(0.25, 0.8, 0.25, 1)';
                        player.style.left = `${coords[index].x}%`;
                        player.style.top = `${coords[index].y}%`;
                        
                        // Limpiar la transición tras finalizar para no interferir con el Drag&Drop
                        setTimeout(() => { player.style.transition = 'transform 0.2s ease'; }, 600);
                    }
                });
                showToast(`Despliegue Táctico ajustado a ${formation}`, "success");
            }
        });
    }

    // --- BOTÓN RESTAURAR POSICIONES ---
    const resetBtn = document.getElementById('reset-positions-btn');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            const coords = tacticalCoords['4-4-2'];
            document.querySelectorAll('.player-node').forEach((player, index) => {
                if (coords[index]) {
                    player.style.transition = 'top 0.6s cubic-bezier(0.25, 0.8, 0.25, 1), left 0.6s cubic-bezier(0.25, 0.8, 0.25, 1)';
                    player.style.left = `${coords[index].x}%`;
                    player.style.top = `${coords[index].y}%`;
                    setTimeout(() => { player.style.transition = 'transform 0.2s ease'; }, 600);
                }
            });
            showToast("Posiciones restauradas a 4-4-2. Recuerda Guardar la Plantilla.", "success");
        });
    }

    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            const originalText = saveBtn.innerText;
            saveBtn.innerText = 'Guardando...';
            saveBtn.disabled = true;

            const playersData = [];
            document.querySelectorAll('.player-node').forEach(card => {
                const id = card.getAttribute('data-id');
                const x = parseFloat(card.style.left) || 0;
                const y = parseFloat(card.style.top) || 0;
                if (id) {
                    playersData.push({ 
                        id: id, 
                        x: x, 
                        y: y,
                        name: card.getAttribute('data-name'),
                        rating: card.getAttribute('data-rating'),
                        pace: card.getAttribute('data-pac'),
                        shooting: card.getAttribute('data-sho'),
                        passing: card.getAttribute('data-pas'),
                        dribbling: card.getAttribute('data-dri'),
                        defending: card.getAttribute('data-def'),
                        physical: card.getAttribute('data-phy'),
                        age: card.getAttribute('data-age'),
                        height: card.getAttribute('data-height'),
                        weight: card.getAttribute('data-weight'),
                        foot: card.getAttribute('data-foot')
                    });
                }
            });

            // Obtener token CSRF (Común en Django. Ajustar según el framework)
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

            fetch('/save-positions/', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ players: playersData })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    showToast("¡Plantilla y Tácticas guardadas exitosamente!", "success");
                } else {
                    showToast("Error al guardar: " + data.message, "error");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast("Fallo de conexión al guardar la pizarra.", "error");
            })
            .finally(() => {
                saveBtn.innerText = originalText;
                saveBtn.disabled = false;
            });
        });
    }

    // --- Lógica del Modal ---
    const modal = document.getElementById('playerModal');
    const closeModalBtn = document.querySelector('.close-modal');
    const players = document.querySelectorAll('.player-node');
    const playerDetailsPanel = document.getElementById('player-details-panel');
    const editSelectedBtn = document.getElementById('edit-selected-btn');

    let selectedPlayerNode = null;

    // --- Calculadora de GRL en el Modal ---
    const statInputs = document.querySelectorAll('.stat-input');
    const ratingDisplay = document.getElementById('playerRatingDisplay');
    const ratingInput = document.getElementById('playerRatingInput');

    function calculateGRL() {
        let total = 0;
        statInputs.forEach(input => {
            total += parseInt(input.value) || 0;
        });
        const grl = Math.round(total / 6) || 0; // Promedio de las 6 stats
        if (ratingDisplay) ratingDisplay.innerText = grl;
        if (ratingInput) ratingInput.value = grl;
    }

    statInputs.forEach(input => {
        input.addEventListener('input', calculateGRL);
    });

    function openEditModal(playerNode) {
        document.getElementById('playerNameInput').value = playerNode.getAttribute('data-name');
        document.getElementById('playerAgeInput').value = playerNode.getAttribute('data-age') || 20;
        document.getElementById('playerHeightInput').value = playerNode.getAttribute('data-height') || 1.80;
        document.getElementById('playerWeightInput').value = playerNode.getAttribute('data-weight') || 75;
        document.getElementById('playerFootInput').value = playerNode.getAttribute('data-foot') || 'Diestro';
        document.getElementById('playerPacInput').value = playerNode.getAttribute('data-pac') || 70;
        document.getElementById('playerShoInput').value = playerNode.getAttribute('data-sho') || 70;
        document.getElementById('playerPasInput').value = playerNode.getAttribute('data-pas') || 70;
        document.getElementById('playerDriInput').value = playerNode.getAttribute('data-dri') || 70;
        document.getElementById('playerDefInput').value = playerNode.getAttribute('data-def') || 70;
        document.getElementById('playerPhyInput').value = playerNode.getAttribute('data-phy') || 70;
        
        calculateGRL();
        modal.style.display = 'flex';
    }

    players.forEach(player => {
        // Inicializar color/rareza de la carta según el GRL cargado
        updateCardRarity(player, parseInt(player.getAttribute('data-rating')) || 75);

        // Clic simple para ver estadísticas en el panel lateral
        player.addEventListener('click', (e) => {
            if (selectedPlayerNode) {
                selectedPlayerNode.classList.remove('selected');
            }
            selectedPlayerNode = player;
            player.classList.add('selected');

            document.getElementById('panel-name').innerText = player.getAttribute('data-name');
            document.getElementById('panel-rating').innerText = player.getAttribute('data-rating');
            document.getElementById('panel-pac').innerText = player.getAttribute('data-pac');
            document.getElementById('panel-sho').innerText = player.getAttribute('data-sho');
            document.getElementById('panel-pas').innerText = player.getAttribute('data-pas');
            document.getElementById('panel-dri').innerText = player.getAttribute('data-dri');
            document.getElementById('panel-def').innerText = player.getAttribute('data-def');
            document.getElementById('panel-phy').innerText = player.getAttribute('data-phy');
            document.getElementById('panel-age').innerText = player.getAttribute('data-age');
            document.getElementById('panel-height').innerText = player.getAttribute('data-height');
            document.getElementById('panel-weight').innerText = player.getAttribute('data-weight');
            document.getElementById('panel-foot').innerText = player.getAttribute('data-foot');

            playerDetailsPanel.style.display = 'block';
        });

        // Doble clic para abrir modal de edición
        player.addEventListener('dblclick', (e) => {
            if (selectedPlayerNode) {
                selectedPlayerNode.classList.remove('selected');
            }
            selectedPlayerNode = player;
            player.classList.add('selected');
            openEditModal(player);
        });
    });

    // Botón de edición dentro del panel lateral
    if (editSelectedBtn) {
        editSelectedBtn.addEventListener('click', () => {
            if (selectedPlayerNode) {
                openEditModal(selectedPlayerNode);
            }
        });
    }

    // Guardar cambios del formulario de edición
    const editPlayerForm = document.getElementById('editPlayerForm');
    if (editPlayerForm) {
        editPlayerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            if (selectedPlayerNode) {
                const playerId = selectedPlayerNode.getAttribute('data-id');
                const submitBtn = editPlayerForm.querySelector('button[type="submit"]');
                const originalBtnText = submitBtn.innerText;
                submitBtn.innerText = "Subiendo...";
                submitBtn.disabled = true;

                const formData = new FormData();
                formData.append('name', document.getElementById('playerNameInput').value);
                formData.append('age', document.getElementById('playerAgeInput').value);
                formData.append('height', document.getElementById('playerHeightInput').value);
                formData.append('weight', document.getElementById('playerWeightInput').value);
                formData.append('foot', document.getElementById('playerFootInput').value);
                formData.append('pace', document.getElementById('playerPacInput').value);
                formData.append('shooting', document.getElementById('playerShoInput').value);
                formData.append('passing', document.getElementById('playerPasInput').value);
                formData.append('dribbling', document.getElementById('playerDriInput').value);
                formData.append('defending', document.getElementById('playerDefInput').value);
                formData.append('physical', document.getElementById('playerPhyInput').value);

                const photoInput = document.getElementById('playerPhotoInput');
                if (photoInput.files.length > 0) {
                    formData.append('photo', photoInput.files[0]);
                }

                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

                fetch(`/edit-player/${playerId}/`, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': csrfToken },
                    body: formData
                })
                .then(r => r.json())
                .then(data => {
                    if (data.status === 'success') {
                        // Actualizar UI con lo devuelto por el servidor
                        selectedPlayerNode.setAttribute('data-name', formData.get('name'));
                        selectedPlayerNode.setAttribute('data-rating', data.rating);
                        selectedPlayerNode.querySelector('.player-name-badge').innerText = formData.get('name');
                        
                        selectedPlayerNode.setAttribute('data-pac', formData.get('pace'));
                        selectedPlayerNode.setAttribute('data-sho', formData.get('shooting'));
                        selectedPlayerNode.setAttribute('data-pas', formData.get('passing'));
                        selectedPlayerNode.setAttribute('data-dri', formData.get('dribbling'));
                        selectedPlayerNode.setAttribute('data-def', formData.get('defending'));
                        selectedPlayerNode.setAttribute('data-phy', formData.get('physical'));
                        selectedPlayerNode.setAttribute('data-age', formData.get('age'));
                        selectedPlayerNode.setAttribute('data-height', formData.get('height'));
                        selectedPlayerNode.setAttribute('data-weight', formData.get('weight'));
                        selectedPlayerNode.setAttribute('data-foot', formData.get('foot'));
                        
                        if (data.photo_url) {
                            selectedPlayerNode.querySelector('.player-jersey').style.backgroundImage = `url('${data.photo_url}')`;
                            const jerseyNumber = selectedPlayerNode.querySelector('.jersey-number');
                            if (jerseyNumber) jerseyNumber.style.display = 'none';
                        }
                        
                        updateCardRarity(selectedPlayerNode, data.rating);
                        showToast("Carta actualizada exitosamente");
                        modal.style.display = 'none';
                        selectedPlayerNode.click(); // Actualiza el panel izquierdo
                    } else {
                        showToast("Error: " + data.message, "error");
                    }
                })
                .finally(() => {
                    submitBtn.innerText = originalBtnText;
                    submitBtn.disabled = false;
                    if(photoInput) photoInput.value = ''; // Limpiar el input file
                });
            }
        });
    }

    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => modal.style.display = 'none');
    }

    window.addEventListener('click', (e) => {
        if (e.target === modal) modal.style.display = 'none';
    });
});
