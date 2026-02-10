// 1. Audio Preview Functionality
const player = document.getElementById('main-player');
const playButtons = document.querySelectorAll('.play-trigger');

playButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevents triggering card click
        const audioSrc = btn.getAttribute('data-src');

        if (player.src.includes(audioSrc) && !player.paused) {
            player.pause();
            btn.innerText = "▶";
        } else {
            player.src = audioSrc;
            player.play();
            // Reset all buttons and set this one to pause
            playButtons.forEach(b => b.innerText = "▶");
            btn.innerText = "⏸";
        }
    });
});

// 2. Smooth Merch Navigation
function navigateToMerch(url) {
    document.body.style.opacity = '0';
    document.body.style.transition = '0.5s';
    setTimeout(() => {
        window.location.href = url;
    }, 500);
}