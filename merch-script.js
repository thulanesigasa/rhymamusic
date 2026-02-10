let cart = [];
let total = 0;

function toggleCart() {
    document.getElementById('cart-drawer').classList.toggle('open');
}

function addToCart(name, price) {
    cart.push({ name, price });
    updateCart();
    // Open cart automatically when item added
    if(!document.getElementById('cart-drawer').classList.contains('open')) {
        toggleCart();
    }
}

function updateCart() {
    const cartItems = document.getElementById('cart-items');
    const cartCount = document.getElementById('cart-count');
    const cartTotal = document.getElementById('cart-total');
    
    cartItems.innerHTML = '';
    total = 0;

    cart.forEach((item, index) => {
        total += item.price;
        cartItems.innerHTML += `
            <div class="cart-item" style="display:flex; justify-content:space-between; margin-bottom:15px;">
                <span>${item.name}</span>
                <span>$${item.price}</span>
            </div>
        `;
    });

    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="empty-msg">Your cart is empty.</p>';
    }

    cartCount.innerText = cart.length;
    cartTotal.innerText = total;
}

// Fade in animation on load
window.onload = () => {
    document.body.style.opacity = "1";
};