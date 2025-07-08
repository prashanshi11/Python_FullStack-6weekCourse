// cart.js

// Load existing cart or initialize new
let cart = JSON.parse(localStorage.getItem("cart")) || [];


// Attach click events to all Add to Cart buttons
document.querySelectorAll('.add-to-cart').forEach(button => {
  button.addEventListener('click', () => {
    const card = button.closest('.product-card');
    const id = card.getAttribute('data-id');
    const name = card.getAttribute('data-name');
    const price = parseFloat(card.getAttribute('data-price'));

    // Check if product already in cart
    const existing = cart.find(item => item.id === id);
    if (existing) {
      existing.quantity += 1;
    } else {
      cart.push({ id, name, price, quantity: 1 });
    }

    // Save to localStorage
    localStorage.setItem("cart", JSON.stringify(cart));

    // Feedback
    alert(`${name} added to cart!`);
  });
});
