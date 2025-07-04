document.querySelectorAll('.game-list li').forEach(function(item, idx) {
    item.addEventListener('click', function() {
        const gameNumber = idx + 1;
        // Store the game number in localStorage for dashboard.html to use
        localStorage.setItem('selectedGame', gameNumber);
        window.location.href = 'dashboard.html';
    });
});
