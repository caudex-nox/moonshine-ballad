const state = { cart: [], products: [], options: null, users: [], categories: [], brands: [] };
const fallbackImage = "/static/img/whisky-fallback.svg";

const money = value => {
  const amount = Number(value);
  if (!Number.isFinite(amount)) return "$0";
  return `$${amount.toLocaleString("es-AR", { maximumFractionDigits: 2 })}`;
};
const escapeHtml = value => String(value ?? "").replace(/[&<>"']/g, char => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
}[char]));
const selectedProfile = key => JSON.parse(localStorage.getItem(`moonshine_${key}`) || "null");
const cartStorageKey = () => {
  const client = selectedProfile("client");
  return client ? `moonshine_cart_${client.id_usuario}` : null;
};

function persistCart() {
  const key = cartStorageKey();
  if (key) localStorage.setItem(key, JSON.stringify(state.cart));
}

function restoreCart() {
  const key = cartStorageKey();
  state.cart = key ? JSON.parse(localStorage.getItem(key) || "[]") : [];
}

function showNotice(message, type = "warning") {
  const notice = document.getElementById("frontNotice");
  if (!notice) return;
  notice.textContent = message;
  notice.className = `front-notice visible ${type}`;
  clearTimeout(showNotice.timeout);
  showNotice.timeout = setTimeout(() => {
    notice.className = "front-notice";
  }, 4500);
}

function activeUser() {
  const client = selectedProfile("client");
  if (client) return { ...client, type: "client" };
  const admin = selectedProfile("admin");
  if (admin) return { ...admin, type: "admin" };
  return null;
}

function requireClient() {
  const user = selectedProfile("client");
  if (!user) {
    showNotice("Seleccioná un cliente en “Usuario activo” antes de añadir productos al carrito.");
    document.getElementById("activeUserSelector")?.focus();
    return false;
  }
  return true;
}

function requireAdmin() {
  const user = selectedProfile("admin");
  if (!user) {
    showNotice("Seleccioná un administrador en “Usuario activo” para gestionar productos.");
    document.getElementById("activeUserSelector")?.focus();
    return false;
  }
  return true;
}

async function api(path, options = {}) {
  const response = await fetch(path, { headers: { "Content-Type": "application/json" }, ...options });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || "No se pudo completar la operación.");
  }
  return response.status === 204 ? null : response.json();
}

function toggleCart() {
  const drawer = document.getElementById("cartDrawer");
  if (!drawer) return;
  drawer.classList.toggle("open");
  document.getElementById("drawerOverlay").style.display = drawer.classList.contains("open") ? "block" : "none";
}

function addToCart(productId) {
  if (!requireClient()) return;
  const product = state.products.find(item => item.id_producto === productId);
  if (!product) {
    showNotice("No se encontró el producto seleccionado.");
    return;
  }
  if (product.stock < 1) {
    showNotice("Este producto no tiene stock disponible.");
    return;
  }
  const item = state.cart.find(entry => entry.id_producto === productId);
  if (item && item.cantidad >= product.stock) {
    showNotice(`Solo hay ${product.stock} unidad${product.stock === 1 ? "" : "es"} disponibles.`);
    return;
  }
  if (item) item.cantidad += 1;
  else state.cart.push({ ...product, cantidad: 1 });
  persistCart();
  updateCartUI();
  toggleCart();
}

function updateCartQuantity(productId, delta) {
  if (!requireClient()) return;
  const item = state.cart.find(entry => entry.id_producto === productId);
  if (!item) return;
  item.cantidad += delta;
  if (item.cantidad <= 0) state.cart = state.cart.filter(entry => entry.id_producto !== productId);
  persistCart();
  updateCartUI();
}

function updateCartUI() {
  const container = document.getElementById("cartItems");
  if (!container) return;
  const count = state.cart.reduce((total, item) => total + item.cantidad, 0);
  document.getElementById("cartCount").textContent = count;
  document.getElementById("cartTotal").textContent = money(state.cart.reduce((total, item) => total + item.precio * item.cantidad, 0));
  container.innerHTML = state.cart.length ? state.cart.map(item => `
    <div class="cart-item"><div><strong>${escapeHtml(item.nombre)}</strong><span>${money(item.precio)}</span></div>
      <div class="quantity"><button onclick="updateCartQuantity(${item.id_producto}, -1)">−</button><span>${item.cantidad}</span><button onclick="updateCartQuantity(${item.id_producto}, 1)">+</button></div>
    </div>`).join("") : '<p class="empty-state">El carrito está vacío.</p>';
}

function filterProducts(category = "All") {
  const grid = document.getElementById("productsGrid");
  if (!grid) return;
  const products = category === "All" ? state.products : state.products.filter(item => item.categoria === category);
  grid.innerHTML = products.length ? products.map(product => `
    <article class="card">
      <img src="${escapeHtml(product.imagen_url || fallbackImage)}" onerror="this.onerror=null;this.src='${fallbackImage}'" class="card-img" alt="${escapeHtml(product.nombre)}" loading="lazy">
      <div class="card-body"><span class="badge">${escapeHtml(product.categoria)}</span>
        <h3 class="card-title">${escapeHtml(product.nombre)}</h3>
        <p class="muted product-meta">${Number(product.abv)}% ABV · ${product.volumen_ml} ml · ${escapeHtml(product.marca)}</p>
        <div class="card-price">${money(product.precio)}</div>
        <button onclick="addToCart(${product.id_producto})" class="btn-primary" ${product.stock < 1 ? "disabled" : ""}>${product.stock ? "Añadir al carrito" : "Sin stock"}</button>
      </div>
    </article>`).join("") : '<p class="empty-state">No hay productos para esta categoría.</p>';
}

async function loadStore() {
  const grid = document.getElementById("productsGrid");
  if (!grid) return;
  try {
    state.products = await api("/catalogo/whiskies");
    const categories = [...new Set(state.products.map(item => item.categoria).filter(Boolean))];
    document.getElementById("categoryFilter").innerHTML += categories.map(category => `<option value="${escapeHtml(category)}">${escapeHtml(category)}</option>`).join("");
    filterProducts();
  } catch (error) { grid.innerHTML = `<p class="error-state">${escapeHtml(error.message)}</p>`; }
}

function fillSelect(id, items, valueKey, label) {
  const select = document.getElementById(id);
  if (select) select.innerHTML = items.map(item => `<option value="${item[valueKey]}">${escapeHtml(label(item))}</option>`).join("");
}

function fillActiveUserSelector() {
  const selector = document.getElementById("activeUserSelector");
  if (!selector || !state.options) return;
  const clientOptions = state.options.clientes.map(user =>
    `<option value="${user.id_usuario}">${escapeHtml(user.nombre)} ${escapeHtml(user.apellido)}</option>`
  ).join("");
  selector.innerHTML = `<option value="">Seleccionar cliente</option>${clientOptions}`;
  const activeClient = selectedProfile("client");
  if (activeClient) selector.value = activeClient.id_usuario;
}

async function loadProfiles() {
  try {
    state.options = await api("/admin/opciones");
    fillActiveUserSelector();
    fillSelect("productCategory", state.options.categorias, "id_categoria", item => item.nombre_categoria);
    fillSelect("productBrand", state.options.marcas, "id_marca", item => item.nombre);
  } catch (error) {
    document.getElementById("activeUserSelector")?.insertAdjacentHTML("afterend", `<small class="error-state">${escapeHtml(error.message)}</small>`);
  }
}

function selectActiveUser(event) {
  const id = event.target.value;
  if (!id || !state.options) {
    localStorage.removeItem("moonshine_client");
    state.cart = [];
    updateCartUI();
    showNotice("Seleccioná un usuario para habilitar las acciones de la tienda.");
    return;
  }
  const profile = state.options.clientes.find(user => String(user.id_usuario) === id);
  if (!profile) return;
  localStorage.setItem("moonshine_client", JSON.stringify(profile));
  restoreCart();
  updateCartUI();
  showNotice(`Usuario activo: ${profile.nombre} ${profile.apellido}.`);
  if (window.location.pathname === "/admin") window.location.href = "/store";
}

function resetProductForm() {
  const form = document.getElementById("productForm");
  if (!form) return;
  form.reset();
  document.getElementById("productId").value = "";
  document.getElementById("formTitle").textContent = "Nuevo producto";
}

function editProduct(productId) {
  if (!requireAdmin()) return;
  const product = state.products.find(item => item.id_producto === productId);
  if (!product) return;
  document.getElementById("productId").value = product.id_producto;
  document.getElementById("formTitle").textContent = "Editar producto";
  ["Name", "Category", "Brand", "Price", "Stock", "Abv", "Volume", "Description", "ImageUrl"].forEach(name => {
    const key = name === "Name" ? "nombre" : name === "Category" ? "id_categoria_fk" : name === "Brand" ? "id_marca_fk" : name === "Price" ? "precio" : name === "Stock" ? "stock" : name === "Abv" ? "abv" : name === "Volume" ? "volumen_ml" : name === "Description" ? "descripcion" : "imagen_url";
    document.getElementById(`product${name}`).value = product[key] ?? "";
  });
  document.querySelector(".product-form-panel").scrollIntoView({ behavior: "smooth", block: "start" });
}

async function loadAdmin() {
  if (!document.getElementById("adminProducts")) return;
  try {
    if (!state.options) await loadProfiles();
    fillSelect("adminSelector", state.options?.admins || [], "id_usuario", user => `${user.nombre} ${user.apellido}`);
    const admin = selectedProfile("admin");
    if (admin) document.getElementById("adminSelector").value = admin.id_usuario;
    state.products = await api("/admin/productos");
    document.getElementById("adminProducts").innerHTML = state.products.map(product => `
      <tr><td><strong>${escapeHtml(product.nombre)}</strong><small>${escapeHtml(product.marca)}</small></td>
        <td><span class="badge">${escapeHtml(product.categoria)}</span></td><td>${money(product.precio)}</td><td>${product.stock} u.</td>
        <td><button class="text-button" onclick="editProduct(${product.id_producto})">Editar</button></td></tr>`).join("");
    await loadAdminEntities();
  } catch (error) { document.getElementById("adminNotice").textContent = error.message; }
}

async function loadAdminEntities() {
  const [users, categories, brands] = await Promise.all([
    api("/admin/usuarios"), api("/admin/categorias"), api("/admin/marcas")
  ]);
  state.users = users;
  state.categories = categories;
  state.brands = brands;
  const usersBody = document.getElementById("adminUsers");
  if (usersBody) usersBody.innerHTML = users.map(user => `
    <tr><td><strong>${escapeHtml(user.nombre)} ${escapeHtml(user.apellido)}</strong><small>${escapeHtml(user.dni)}</small></td>
      <td>${escapeHtml(user.email)}</td><td><span class="badge">${escapeHtml(user.rol)}</span></td>
      <td>${escapeHtml(user.tel_movil || "—")}</td><td><button class="text-button" onclick="editUser(${user.id_usuario})">Editar</button></td></tr>`).join("");
  const categoriesBody = document.getElementById("adminCategories");
  if (categoriesBody) categoriesBody.innerHTML = categories.map(category => `
    <tr><td><strong>${escapeHtml(category.nombre_categoria)}</strong></td><td>${escapeHtml(category.descripcion || "—")}</td>
      <td><button class="text-button" onclick="editCategory(${category.id_categoria})">Editar</button></td></tr>`).join("");
  const brandsBody = document.getElementById("adminBrands");
  if (brandsBody) brandsBody.innerHTML = brands.map(brand => `
    <tr><td><strong>${escapeHtml(brand.nombre)}</strong></td><td>${escapeHtml(brand.pais_origen)}</td>
      <td><button class="text-button" onclick="editBrand(${brand.id_marca})">Editar</button></td></tr>`).join("");
}

function editUser(userId) {
  if (!requireAdmin()) return;
  const user = state.users.find(item => item.id_usuario === userId);
  if (!user) return;
  document.getElementById("userId").value = user.id_usuario;
  document.getElementById("userFormTitle").textContent = "Editar usuario";
  document.getElementById("userName").value = user.nombre;
  document.getElementById("userLastName").value = user.apellido;
  document.getElementById("userEmail").value = user.email;
  document.getElementById("userDni").value = user.dni;
  document.getElementById("userDni").disabled = true;
  document.getElementById("userRole").value = user.id_rol_fk;
  document.getElementById("userMobile").value = user.tel_movil || "";
  document.querySelector("[data-admin-panel='users'] .admin-edit-panel").scrollIntoView({ behavior: "smooth" });
}

function editCategory(categoryId) {
  if (!requireAdmin()) return;
  const category = state.categories.find(item => item.id_categoria === categoryId);
  if (!category) return;
  document.getElementById("categoryForm").dataset.id = category.id_categoria;
  document.getElementById("categoryFormTitle").textContent = "Editar categoría";
  document.getElementById("categoryName").value = category.nombre_categoria;
  document.getElementById("categoryDescription").value = category.descripcion || "";
  document.querySelector("[data-admin-panel='categories'] .admin-edit-panel").scrollIntoView({ behavior: "smooth" });
}

function editBrand(brandId) {
  if (!requireAdmin()) return;
  const brand = state.brands.find(item => item.id_marca === brandId);
  if (!brand) return;
  document.getElementById("brandForm").dataset.id = brand.id_marca;
  document.getElementById("brandFormTitle").textContent = "Editar marca";
  document.getElementById("brandName").value = brand.nombre;
  document.getElementById("brandCountry").value = brand.pais_origen;
  document.querySelector("[data-admin-panel='brands'] .admin-edit-panel").scrollIntoView({ behavior: "smooth" });
}

function resetUserForm() {
  document.getElementById("userForm")?.reset();
  document.getElementById("userId").value = "";
  document.getElementById("userDni").disabled = false;
  document.getElementById("userFormTitle").textContent = "Crear usuario";
}

function resetNamedForm(formId, titleId, title) {
  const form = document.getElementById(formId);
  form?.reset();
  if (form) delete form.dataset.id;
  document.getElementById(titleId).textContent = title;
}

function selectAdmin(event) {
  const profile = state.options?.admins.find(user => String(user.id_usuario) === event.target.value);
  if (!profile) return;
  localStorage.setItem("moonshine_admin", JSON.stringify(profile));
  showNotice(`Administrador activo: ${profile.nombre} ${profile.apellido}.`, "info");
}

function switchAdminSection(event) {
  const section = event.currentTarget.dataset.adminSection;
  document.querySelectorAll(".admin-tab").forEach(tab => tab.classList.toggle("active", tab === event.currentTarget));
  document.querySelectorAll("[data-admin-panel]").forEach(panel => panel.classList.toggle("hidden", panel.dataset.adminPanel !== section));
}

async function submitAdminForm(event, path, successMessage, method = "POST") {
  event.preventDefault();
  if (!requireAdmin()) return;
  try {
    await api(path, { method, body: JSON.stringify(Object.fromEntries(new FormData(event.currentTarget))) });
    document.getElementById("adminNotice").textContent = successMessage;
    event.currentTarget.reset();
    await loadProfiles();
    await loadAdmin();
  } catch (error) {
    document.getElementById("adminNotice").textContent = error.message;
  }
}

async function saveProduct(event) {
  event.preventDefault();
  if (!requireAdmin()) return;
  const id = document.getElementById("productId").value;
  const payload = {
    nombre: document.getElementById("productName").value,
    id_categoria_fk: Number(document.getElementById("productCategory").value),
    id_marca_fk: Number(document.getElementById("productBrand").value),
    precio: Number(document.getElementById("productPrice").value),
    stock: Number(document.getElementById("productStock").value),
    abv: Number(document.getElementById("productAbv").value),
    volumen_ml: Number(document.getElementById("productVolume").value),
    descripcion: document.getElementById("productDescription").value || null,
    imagen_url: document.getElementById("productImageUrl").value.trim() || null,
    id_proveedor_fk: null
  };
  if (!Number.isFinite(payload.precio) || payload.precio < 0) {
    showNotice("Ingresá un precio válido sin el símbolo “$”.");
    document.getElementById("productPrice").focus();
    return;
  }
  try {
    await api(id ? `/admin/productos/${id}` : "/admin/productos", { method: id ? "PUT" : "POST", body: JSON.stringify(payload) });
    document.getElementById("adminNotice").textContent = "Producto guardado correctamente.";
    resetProductForm();
    await loadAdmin();
  } catch (error) { document.getElementById("adminNotice").textContent = error.message; }
}

function checkout() {
  if (!requireClient()) return;
  if (!state.cart.length) {
    showNotice("Agregá al menos un producto antes de finalizar la compra.");
    return;
  }
  const client = selectedProfile("client");
  api("/catalogo/ventas", {
    method: "POST",
    body: JSON.stringify({
      id_cliente: client.id_usuario,
      metodo_pago: "Demo",
      items: state.cart.map(item => ({
        id_producto: item.id_producto,
        cantidad: item.cantidad
      }))
    })
  }).then(() => {
    state.cart = [];
    persistCart();
    updateCartUI();
    showNotice("¡Compra realizada con éxito!", "success");
    document.getElementById("cartDrawer")?.classList.remove("open");
    const overlay = document.getElementById("drawerOverlay");
    if (overlay) overlay.style.display = "none";
    loadStore();
  }).catch(error => {
    showNotice(error.message);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("activeUserSelector")?.addEventListener("change", selectActiveUser);
  document.getElementById("adminSelector")?.addEventListener("change", selectAdmin);
  document.querySelectorAll(".admin-tab").forEach(tab => tab.addEventListener("click", switchAdminSection));
  document.getElementById("categoryFilter")?.addEventListener("change", event => filterProducts(event.target.value));
  document.getElementById("newProductButton")?.addEventListener("click", resetProductForm);
  document.getElementById("cancelProductButton")?.addEventListener("click", resetProductForm);
  document.getElementById("productForm")?.addEventListener("submit", saveProduct);
  document.getElementById("newUserButton")?.addEventListener("click", resetUserForm);
  document.getElementById("cancelUserButton")?.addEventListener("click", resetUserForm);
  document.getElementById("newCategoryButton")?.addEventListener("click", () => resetNamedForm("categoryForm", "categoryFormTitle", "Nueva categoría"));
  document.getElementById("cancelCategoryButton")?.addEventListener("click", () => resetNamedForm("categoryForm", "categoryFormTitle", "Nueva categoría"));
  document.getElementById("newBrandButton")?.addEventListener("click", () => resetNamedForm("brandForm", "brandFormTitle", "Nueva marca"));
  document.getElementById("cancelBrandButton")?.addEventListener("click", () => resetNamedForm("brandForm", "brandFormTitle", "Nueva marca"));
  document.getElementById("categoryForm")?.addEventListener("submit", event => {
    const form = event.currentTarget;
    const id = form.dataset.id;
    submitAdminForm(event, id ? `/admin/categorias/${id}` : "/admin/categorias", "Categoría guardada correctamente", id ? "PUT" : "POST");
  });
  document.getElementById("brandForm")?.addEventListener("submit", event => {
    const form = event.currentTarget;
    const id = form.dataset.id;
    submitAdminForm(event, id ? `/admin/marcas/${id}` : "/admin/marcas", "Marca guardada correctamente", id ? "PUT" : "POST");
  });
  document.getElementById("userForm")?.addEventListener("submit", event => {
    const fields = {
      id_rol_fk: Number(document.getElementById("userRole").value),
      dni: document.getElementById("userDni").value,
      nombre: document.getElementById("userName").value,
      apellido: document.getElementById("userLastName").value,
      email: document.getElementById("userEmail").value,
      tel_movil: document.getElementById("userMobile").value || null,
      ciudad: document.getElementById("userCity").value,
      provincia: document.getElementById("userProvince").value,
      codigo_postal: document.getElementById("userPostalCode").value,
      calle: document.getElementById("userStreet").value,
      numero: document.getElementById("userNumber").value
    };
    event.preventDefault();
    if (!requireAdmin()) return;
    const id = document.getElementById("userId").value;
    const updateFields = { id_rol_fk: fields.id_rol_fk, nombre: fields.nombre, apellido: fields.apellido, email: fields.email, tel_movil: fields.tel_movil };
    api(id ? `/admin/usuarios/${id}` : "/admin/usuarios", { method: id ? "PUT" : "POST", body: JSON.stringify(id ? updateFields : fields) })
      .then(() => { document.getElementById("adminNotice").textContent = "Usuario guardado correctamente."; resetUserForm(); loadProfiles(); loadAdminEntities(); })
      .catch(error => { document.getElementById("adminNotice").textContent = error.message; });
  });
  restoreCart();
  updateCartUI();
  loadProfiles();
  loadStore();
  loadAdmin();
});
