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
        // Added a button with onclick="removeFromCart(${index})"
        cartItems.innerHTML += `
            <div class="cart-item" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; border-bottom: 1px solid var(--glass); padding-bottom: 5px;">
                <div>
                    <span style="display:block; font-weight:bold;">${item.name}</span>
                    <span style="color:var(--bronze);">$${item.price}</span>
                </div>
                <button onclick="removeFromCart(${index})" style="background:none; border:none; color:red; cursor:pointer; font-size:1.2rem;">&times;</button>
            </div>
        `;
    });

    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="empty-msg">Your cart is empty.</p>';
    }

    cartCount.innerText = cart.length;
    cartTotal.innerText = total;
}

// NEW FUNCTION: Removes item by its position in the array
function removeFromCart(index) {
    cart.splice(index, 1); // Removes 1 element at the specified index
    updateCart();          // Refresh the UI
}

// Fade in animation on load
window.onload = () => {
    document.body.style.opacity = "1";
};