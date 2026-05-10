// Archivo: static/js/pitch.js
// Etiqueta: Lógica de UI para la pizarra y guardado de formaciones

document.addEventListener('DOMContentLoaded', () => {
    const formationSelect = document.getElementById('formation-select');
    const saveBtn = document.getElementById('save-team-btn');

    if (formationSelect) {
        formationSelect.addEventListener('change', (e) => {
            const formation = e.target.value;
            if (formation) {
                console.log(`Cambiando a formación: ${formation}`);
            }
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
                    playersData.push({ id: id, x: x, y: y });
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
                    alert("¡Posiciones guardadas correctamente en la base de datos!");
                } else {
                    alert("Error al guardar: " + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("Ocurrió un error al guardar las posiciones.");
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
                // 1. Actualizar atributos internamente en el HTML
                selectedPlayerNode.setAttribute('data-name', document.getElementById('playerNameInput').value);
                selectedPlayerNode.setAttribute('data-age', document.getElementById('playerAgeInput').value);
                selectedPlayerNode.setAttribute('data-height', document.getElementById('playerHeightInput').value);
                selectedPlayerNode.setAttribute('data-weight', document.getElementById('playerWeightInput').value);
                selectedPlayerNode.setAttribute('data-foot', document.getElementById('playerFootInput').value);
                selectedPlayerNode.setAttribute('data-pac', document.getElementById('playerPacInput').value);
                selectedPlayerNode.setAttribute('data-sho', document.getElementById('playerShoInput').value);
                selectedPlayerNode.setAttribute('data-pas', document.getElementById('playerPasInput').value);
                selectedPlayerNode.setAttribute('data-dri', document.getElementById('playerDriInput').value);
                selectedPlayerNode.setAttribute('data-def', document.getElementById('playerDefInput').value);
                selectedPlayerNode.setAttribute('data-phy', document.getElementById('playerPhyInput').value);
                selectedPlayerNode.setAttribute('data-rating', document.getElementById('playerRatingInput').value);

                // 2. Actualizar diseño de la ficha del jugador en la cancha
                selectedPlayerNode.querySelector('.player-name-badge').innerText = document.getElementById('playerNameInput').value;
                const jerseyNumber = selectedPlayerNode.querySelector('.jersey-number');
                if(jerseyNumber) jerseyNumber.innerText = document.getElementById('playerRatingInput').value;

                // 3. Forzar un clic en el jugador para que se actualice la tarjeta de la izquierda
                selectedPlayerNode.click();

                modal.style.display = 'none';
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
