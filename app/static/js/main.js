// Estado local de la app
const state = {
  cart: [],
  products: [
    { id_producto: 1, nombre: "Lagavulin 16 Años", categoria: "Single Malt", abv: 43.0, volumen_ml: 750, precio: 145000, stock: 8, imagen_url: "https://images.unsplash.com/photo-1527281400683-1aae777175f8?w=500" },
    { id_producto: 2, nombre: "Woodford Reserve", categoria: "Bourbon", abv: 45.2, volumen_ml: 750, precio: 68000, stock: 15, imagen_url: "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=500" },
    { id_producto: 3, nombre: "Hibiki Japanese Harmony", categoria: "Blended", abv: 43.0, volumen_ml: 700, precio: 210000, stock: 4, imagen_url: "https://images.unsplash.com/photo-1563227812-0ea4c22e6cc8?w=500" }
  ]
};

// Carrito
function toggleCart() {
  const drawer = document.getElementById("cartDrawer");
  const overlay = document.getElementById("drawerOverlay");
  drawer.classList.toggle("open");
  overlay.style.display = drawer.classList.contains("open") ? "block" : "none";
}

function addToCart(productId) {
  const prod = state.products.find(p => p.id_producto === productId);
  if (!prod) return;

  const item = state.cart.find(i => i.id_producto === productId);
  if (item) {
    item.cantidad += 1;
  } else {
    state.cart.push({ ...prod, cantidad: 1 });
  }

  updateCartUI();
  toggleCart();
}

function updateCartQuantity(productId, delta) {
  const item = state.cart.find(i => i.id_producto === productId);
  if (!item) return;

  item.cantidad += delta;
  if (item.cantidad <= 0) {
    state.cart = state.cart.filter(i => i.id_producto !== productId);
  }
  updateCartUI();
}

function updateCartUI() {
  const container = document.getElementById("cartItems");
  const badge = document.getElementById("cartCount");
  const totalElem = document.getElementById("cartTotal");

  const totalCount = state.cart.reduce((acc, i) => acc + i.cantidad, 0);
  const totalPrice = state.cart.reduce((acc, i) => acc + (i.precio * i.cantidad), 0);

  badge.textContent = totalCount;
  totalElem.textContent = `$${totalPrice.toLocaleString("es-AR")}`;

  if (state.cart.length === 0) {
    container.innerHTML = `<p style="color: var(--text-muted); text-align: center; margin-top: 2rem;">El carrito está vacío.</p>`;
    return;
  }

  container.innerHTML = state.cart.map(item => `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.75rem;">
      <div>
        <div style="font-weight: 600; font-size: 0.9rem;">${item.nombre}</div>
        <div style="color: var(--accent-gold); font-size: 0.85rem;">$${item.precio.toLocaleString("es-AR")}</div>
      </div>
      <div style="display: flex; align-items: center; gap: 0.5rem;">
        <button onclick="updateCartQuantity(${item.id_producto}, -1)" class="nav-btn" style="padding: 0.2rem 0.5rem;">-</button>
        <span style="font-size: 0.9rem;">${item.cantidad}</span>
        <button onclick="updateCartQuantity(${item.id_producto}, 1)" class="nav-btn" style="padding: 0.2rem 0.5rem;">+</button>
      </div>
    </div>
  `).join('');
}

// Filtro de Tienda
function filterProducts(category = 'All') {
  const grid = document.getElementById("productsGrid");
  if (!grid) return;

  const filtered = category === 'All' 
    ? state.products 
    : state.products.filter(p => p.categoria === category);

  grid.innerHTML = filtered.map(p => `
    <div class="card">
      <img src="${p.imagen_url}" class="card-img" alt="${p.nombre}">
      <div class="card-body">
        <span class="badge badge-amber">${p.categoria}</span>
        <h3 class="card-title">${p.nombre}</h3>
        <p style="color: var(--text-muted); font-size: 0.8rem; margin-bottom: 0.5rem;">${p.abv}% ABV | ${p.volumen_ml} ml</p>
        <div class="card-price" style="margin-bottom: 1rem;">$${p.precio.toLocaleString("es-AR")}</div>
        <button onclick="addToCart(${p.id_producto})" class="btn-primary">Añadir al Carrito</button>
      </div>
    </div>
  `).join('');
}

// Inicialización de escuchadores
document.addEventListener("DOMContentLoaded", () => {
  filterProducts();
});