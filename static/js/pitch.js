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
            document.querySelectorAll('.player-card').forEach(card => {
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
    const players = document.querySelectorAll('.player-card');

    players.forEach(player => {
        player.addEventListener('dblclick', (e) => {
            const playerName = player.querySelector('.player-name').innerText;
            const playerRating = player.querySelector('.player-rating').innerText;
            
            document.getElementById('playerNameInput').value = playerName;
            document.getElementById('playerRatingInput').value = playerRating;
            
            modal.style.display = 'flex';
        });
    });

    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => modal.style.display = 'none');
    }

    window.addEventListener('click', (e) => {
        if (e.target === modal) modal.style.display = 'none';
    });
});
