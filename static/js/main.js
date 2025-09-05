// main.js
// Funções de UI (menu), carrinho (localStorage) e integração de checkout com Flask.

// ----------------------
// Menu mobile
// ----------------------
const menuToggle = document.getElementById('menuToggle');
const menu = document.getElementById('menu');
if (menuToggle && menu) {
  menuToggle.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    menuToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
}

// ----------------------
// Carrinho (armazenado no localStorage)
// ----------------------
const CART_KEY = 'meu_carrinho_v1';

function loadCart() {
  try { return JSON.parse(localStorage.getItem(CART_KEY)) || []; } catch (_) { return []; }
}
function saveCart(items) {
  localStorage.setItem(CART_KEY, JSON.stringify(items));
}
function addToCart(item) {
  const cart = loadCart();
  const idx = cart.findIndex(i => i.id === item.id);
  if (idx >= 0) { cart[idx].qty += 1; } else { cart.push({ ...item, qty: 1 }); }
  saveCart(cart);
  alert('Adicionado ao carrinho!');
}
function removeFromCart(id) {
  const cart = loadCart().filter(i => i.id !== id);
  saveCart(cart);
  renderCart();
}
function updateQty(id, qty) {
  const cart = loadCart();
  const item = cart.find(i => i.id === id);
  if (item) {
    item.qty = Math.max(1, parseInt(qty || '1', 10));
    saveCart(cart);
    renderCart();
  }
}
function cartTotal() {
  return loadCart().reduce((sum, i) => sum + i.price * i.qty, 0);
}

// Botões "Adicionar ao carrinho" na loja
const productList = document.getElementById('productList');
if (productList) {
  productList.addEventListener('click', (e) => {
    const btn = e.target.closest('.add-to-cart');
    if (!btn) return;
    const card = btn.closest('.card');
    const item = {
      id: card.dataset.id,
      title: card.dataset.title,
      price: parseFloat(card.dataset.price),
    };
    addToCart(item);
  });
}

// Render do carrinho em /cart
function renderCart() {
  const el = document.getElementById('cartContainer');
  if (!el) return;
  const cart = loadCart();
  if (!cart.length) {
    el.innerHTML = '<p>Seu carrinho está vazio.</p>';
    return;
  }
  const rows = cart.map(i => `
    <div class="card" style="display:flex; align-items:center; gap:10px;">
      <div style="flex:1;">
        <strong>${i.title}</strong><br/>
        <small>R$ ${i.price.toFixed(2)}</small>
      </div>
      <label>Qtd: <input type="number" min="1" value="${i.qty}" data-id="${i.id}" class="qty" style="width:64px;" /></label>
      <button class="btn outline remove" data-id="${i.id}">Remover</button>
    </div>
  `).join('');
  el.innerHTML = rows + `<p><strong>Total: R$ ${cartTotal().toFixed(2)}</strong></p>`;
}

const cartContainer = document.getElementById('cartContainer');
if (cartContainer) {
  renderCart();
  cartContainer.addEventListener('input', (e) => {
    const qty = e.target.closest('.qty');
    if (qty) updateQty(qty.dataset.id, qty.value);
  });
  cartContainer.addEventListener('click', (e) => {
    const rm = e.target.closest('.remove');
    if (rm) removeFromCart(rm.dataset.id);
  });
}

const clearBtn = document.getElementById('clearCart');
if (clearBtn) {
  clearBtn.addEventListener('click', () => {
    saveCart([]);
    renderCart();
  });
}

// ----------------------
// Checkout — envia pedido para o backend Flask
// ----------------------
function renderCheckoutSummary() {
  const wrap = document.getElementById('checkoutSummary');
  const totalEl = document.getElementById('checkoutTotal');
  if (!wrap || !totalEl) return;
  const cart = loadCart();
  if (!cart.length) { wrap.innerHTML = '<p>Seu carrinho está vazio.</p>'; totalEl.textContent = '0,00'; return; }
  wrap.innerHTML = cart.map(i => `<div><strong>${i.title}</strong> × ${i.qty} — R$ ${(i.price * i.qty).toFixed(2)}</div>`).join('');
  totalEl.textContent = cartTotal().toFixed(2);
}
renderCheckoutSummary();

const checkoutForm = document.getElementById('checkoutForm');
if (checkoutForm) {
  checkoutForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = new FormData(checkoutForm);
    const customer = {
      name: form.get('name').trim(),
      email: form.get('email').trim(),
      phone: (form.get('phone') || '').trim(),
    };
    const items = loadCart();
    const total = cartTotal();
    const msg = document.getElementById('checkoutMsg');

    if (!customer.name || !customer.email || !items.length) {
      msg.textContent = 'Preencha seus dados e adicione itens ao carrinho.';
      return;
    }

    try {
      const res = await fetch('/checkout', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ customer, items, total })
      });
      const data = await res.json();
      if (data.ok) {
        msg.textContent = 'Pedido enviado com sucesso! Você receberá um e-mail em breve.';
        saveCart([]); // limpa carrinho
        renderCheckoutSummary();
      } else {
        msg.textContent = data.message || 'Não foi possível enviar o pedido.';
      }
    } catch (err) {
      msg.textContent = 'Erro de conexão. Tente novamente em instantes.';
    }
  });
}
