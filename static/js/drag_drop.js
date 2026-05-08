// Archivo: static/js/drag_drop.js
// Etiqueta: Lógica de arrastrar y soltar (Drag & Drop) de jugadores

document.addEventListener('DOMContentLoaded', () => {
    const players = document.querySelectorAll('.player-card');
    const pitch = document.getElementById('pitch');

    let isDragging = false;
    let currentDragged = null;
    let offsetX = 0;
    let offsetY = 0;

    players.forEach(player => {
        player.addEventListener('mousedown', (e) => {
            isDragging = true;
            currentDragged = player;
            
            const rect = player.getBoundingClientRect();
            offsetX = e.clientX - rect.left;
            offsetY = e.clientY - rect.top;
            
            player.style.cursor = 'grabbing';
            player.style.zIndex = 1000;
            
            // Evitar comportamiento por defecto (como selección de texto o arrastre nativo de imágenes)
            e.preventDefault();
        });
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDragging || !currentDragged) return;

        const pitchRect = pitch.getBoundingClientRect();
        
        let newX = e.clientX - pitchRect.left - offsetX + (currentDragged.offsetWidth / 2);
        let newY = e.clientY - pitchRect.top - offsetY + (currentDragged.offsetHeight / 2);
        
        if (newX < 0) newX = 0;
        if (newY < 0) newY = 0;
        if (newX > pitchRect.width) newX = pitchRect.width;
        if (newY > pitchRect.height) newY = pitchRect.height;
        
        const xPercent = (newX / pitchRect.width) * 100;
        const yPercent = (newY / pitchRect.height) * 100;

        currentDragged.style.left = `${xPercent}%`;
        currentDragged.style.top = `${yPercent}%`;
    });

    document.addEventListener('mouseup', () => {
        if (currentDragged) {
            currentDragged.style.cursor = 'grab';
            currentDragged.style.zIndex = '';
        }
        isDragging = false;
        currentDragged = null;
    });
});
