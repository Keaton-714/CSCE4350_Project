// This file contains all the logic for each tab
(function () 
{
  'use strict';

  // Helpers
  const $ = id => document.getElementById(id);
  const money = n => '$' + Number(n).toFixed(2);

  // Safe DOM builder
  function el(tag, props = {}, ...children) {
    const node = document.createElement(tag);
    Object.entries(props).forEach(([k, v]) => k === 'class' ? node.className = v : node[k] = v);
    children.forEach(c => node.append(c));
    return node;
  }

  let toastTimer;
  function toast(msg, isError = false) {
    const t = $('toast');
    t.textContent = msg;
    t.className = 'toast' + (isError ? ' error' : '');
    t.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => t.hidden = true, 2800);
  }

  // ---------- State ----------
  // Parts and stock always come from the backend. The cart lives in memory
  // (it is tied to the selected store). Orders are kept in localStorage until
  // the backend has an orders endpoint.
  const ORDERS_KEY = 'autoparts_' + document.body.dataset.user + '_orders';

  function loadOrders() {
    try { return JSON.parse(localStorage.getItem(ORDERS_KEY)) || []; }
    catch (e) { return []; }
  }
  function saveOrders() {
    try { localStorage.setItem(ORDERS_KEY, JSON.stringify(orders)); } catch (e) {}
  }

  let parts = [];              // [{ id, name, description, price, category, stock }]
  let cart = {};               // { partId: quantity }
  let orders = loadOrders();
  let detailPart = null;

  const partById = id => parts.find(p => p.id === id);

  // ---------- API ----------
  async function loadStores() {
    const response = await fetch('/api/stores');
    const stores = await response.json();
    const select = $('store-select');
    stores.forEach(store => select.add(new Option(`${store.city}, ${store.state}`, store.store_id)));
  }

  async function loadParts(storeId) {
    const response = await fetch(`/api/stores/${storeId}/inventory`);
    const inventory = await response.json();

    parts = inventory.map(part => ({
      id: part.part_id,
      name: part.name,
      description: part.description || '',
      price: part.price,
      category: part.category,
      stock: part.stock_quantity
    }));

    const category = $('category');
    category.replaceChildren(new Option('All categories', ''));
    [...new Set(parts.map(p => p.category))].sort().forEach(c => category.add(new Option(c, c)));

    renderParts();
    renderCart();
  }

  // Tabs
  const tabs = document.querySelectorAll('[role="tab"]');

  function showTab(tab) {
    tabs.forEach(t => {
      const selected = t === tab;
      t.setAttribute('aria-selected', selected);
      $(t.getAttribute('aria-controls')).hidden = !selected;
    });
    if (tab.id === 'tab-cart') renderCart();
    if (tab.id === 'tab-history') renderOrders();
  }

  tabs.forEach(t => t.addEventListener('click', () => showTab(t)));

  // Browse
  const remaining = p => Math.max(0, p.stock - (cart[p.id] || 0));

  // checks the stock and gives live updated to user
  function stockLabel(n, inCart = 0) {
    if (n <= 0 && inCart > 0) return el('span', { class: 'stock-out', textContent: 'None left'});
    if (n <= 0) return el('span', { class: 'stock-out', textContent: 'Out of stock' });
    if (n <= 10) return el('span', { class: 'stock-low', textContent: 'Only ' + n + ' left in stock' });
    return el('span', { class: 'stock-ok', textContent: n + ' in stock' });
  }

  function renderParts() {
    const q = $('search').value.trim().toLowerCase();
    const cat = $('category').value;
    const list = parts.filter(p =>
      (!cat || p.category === cat) &&
      (!q || p.name.toLowerCase().includes(q) || p.description.toLowerCase().includes(q)));

    const grid = $('parts-grid');
    grid.replaceChildren();
    $('parts-empty').hidden = list.length > 0;
    list.forEach(p => {
      const inCart = cart[p.id] || 0;
      const maxedOut = p.stock > 0 && inCart >= p.stock;
      const add = el('button', {
        class: 'primary',
        textContent: maxedOut ? 'Max in cart' : 'Add to cart',
        disabled: p.stock <= 0 || maxedOut
      });
      add.addEventListener('click', () => addToCart(p.id, 1));
      const details = el('button', { class: 'secondary', textContent: 'Details' });
      details.addEventListener('click', () => openDetails(p.id));
      grid.append(el('div', { class: 'card' },
        el('h3', { textContent: p.name }),
        el('span', { class: 'cat', textContent: p.category }),
        el('span', { class: 'price', textContent: money(p.price) }),
        stockLabel(remaining(p), cart[p.id] || 0),
        el('div', { class: 'actions' }, details, add)));
    });
  }

  $('search').addEventListener('input', renderParts);
  $('category').addEventListener('change', renderParts);

  $('store-select').addEventListener('change', function () {
    cart = {};   // the cart belongs to one store, so clear it on change
    if (this.value) {
      loadParts(this.value);
    } else {
      parts = [];
      $('category').replaceChildren(new Option('All categories', ''));
      renderParts();
      renderCart();
    }
  });

  // Part details
  function openDetails(id) {
    const p = partById(id);
    detailPart = p;
    $('d-name').textContent = p.name;
    $('d-desc').textContent = p.description || 'No description available.';
    $('d-id').textContent = p.id;
    $('d-cat').textContent = p.category;
    $('d-price').textContent = money(p.price);
    const inCart = cart[p.id] || 0;
    const available = Math.max(0, p.stock - inCart);
    $('d-stock').textContent = p.stock <= 0 ? 'Out of stock'
      : available + ' available' + (inCart ? ' (' + inCart + ' already in your cart)' : '');
    $('d-qty').value = available > 0 ? 1 : 0;
    $('d-qty').min = available > 0 ? 1 : 0;
    $('d-qty').max = available;
    $('d-qty').disabled = available <= 0;
    $('d-add').disabled = available <= 0;
    $('part-dialog').showModal();
  }

  // change number of stock 
  $('d-close').addEventListener('click', () => $('part-dialog').close());
  $('d-qty').addEventListener('change', () => {
    const max = parseInt($('d-qty').max) || 0;
    let q = parseInt($('d-qty').value) || 1;
    if (q > max) { q = max; toast('Only ' + max + ' available to add.', true); }
    $('d-qty').value = Math.max(q, max > 0 ? 1 : 0);
  });
  $('d-add').addEventListener('click', () => {
    const qty = Math.max(1, parseInt($('d-qty').value) || 1);
    if (addToCart(detailPart.id, qty)) $('part-dialog').close();
  });

  // Cart 
  function setQty(id, qty) {
    const p = partById(id);
    if (qty > p.stock) { qty = p.stock; toast('Only ' + p.stock + ' in stock - quantity adjusted.', true); }
    if (qty <= 0) { delete cart[id]; } else { cart[id] = qty; }
    renderCart();
    renderParts();
  }

  function addToCart(id, qty) {
    const p = partById(id);
    if (p.stock <= 0) { toast(p.name + ' is out of stock.', true); return false; }
    const inCart = cart[id] || 0;
    if (inCart >= p.stock) {
      toast('You already have all ' + p.stock + ' in stock in your cart.', true);
      return false;
    }
    if (inCart + qty > p.stock) {
      toast('Only ' + p.stock + ' in stock (' + inCart + ' already in your cart).', true);
      return false;
    }
    setQty(id, inCart + qty);
    toast('Added ' + p.name + ' to cart');
    return true;
  }

  function cartTotals() {
    let total = 0, count = 0;
    Object.entries(cart).forEach(([id, qty]) => { total += partById(+id).price * qty; count += qty; });
    return { total, count };
  }

  function renderCart() {
    const { total, count } = cartTotals();
    $('cart-badge').textContent = count;
    $('cart-badge').hidden = count === 0;
    const empty = count === 0;
    $('cart-empty').hidden = !empty;
    $('cart-table').hidden = empty;
    $('cart-actions').hidden = empty;

    const body = $('cart-body');
    body.replaceChildren();
    Object.entries(cart).forEach(([sid, qty]) => {
      const p = partById(+sid);
      const minus = el('button', { class: 'secondary', textContent: '-', ariaLabel: 'Decrease quantity' });
      const plus = el('button', { class: 'secondary', textContent: '+', ariaLabel: 'Increase quantity', disabled: qty >= p.stock });
      const input = el('input', { type: 'number', min: 1, max: p.stock, value: qty });
      const remove = el('button', { class: 'secondary', textContent: 'Remove' });
      minus.addEventListener('click', () => setQty(p.id, qty - 1));
      plus.addEventListener('click', () => setQty(p.id, qty + 1));
      input.addEventListener('change', () => setQty(p.id, parseInt(input.value) || 0));
      remove.addEventListener('click', () => setQty(p.id, 0));
      body.append(el('tr', {},
        el('td', {}, el('strong', { textContent: p.name }), el('br'), el('span', { class: 'cat', textContent: p.category }), el('br'), el('span', { class: 'cat', textContent: remaining(p) + ' more available (' + p.stock + ' in stock)' })),
        el('td', { class: 'num', textContent: money(p.price) }),
        el('td', {}, el('span', { class: 'qty' }, minus, input, plus)),
        el('td', { class: 'num', textContent: money(p.price * qty) }),
        el('td', {}, remove)));
    });
    $('cart-total').textContent = money(total);
  }

  $('clear-cart').addEventListener('click', () => { cart = {}; renderCart(); });

  //  Checkout 
  $('checkout').addEventListener('click', () => {
    const { total } = cartTotals();
    if (!confirm('Place order for ' + money(total) + '?')) return;

    // re-check stock, then build the order
    for (const [sid, qty] of Object.entries(cart)) {
      const p = partById(+sid);
      if (p.stock < qty) {
        toast('Not enough stock for ' + p.name + ' (only ' + p.stock + ' left).', true);
        renderCart();
        return;
      }
    }
    const items = Object.entries(cart).map(([sid, qty]) => {
      const p = partById(+sid);
      p.stock -= qty; // local 
      return { name: p.name, quantity: qty, unit_price: p.price };
    });
    const order = {
      order_id: orders.length ? Math.max(...orders.map(o => o.order_id)) + 1 : 1,
      order_date: new Date().toISOString().slice(0, 10),
      status: 'Pending', items, total
    };
    orders.unshift(order);
    cart = {};
    saveOrders();
    toast('Order #' + order.order_id + ' placed!');
    renderParts();
    showTab($('tab-history'));
  });

  // Purchase history 
  function renderOrders() {
    const box = $('orders');
    box.replaceChildren();
    if (!orders.length) { box.append(el('p', { textContent: 'No orders yet.' })); return; }
    orders.forEach(o => {
      const rows = o.items.map(i => el('tr', {},
        el('td', { textContent: i.name }),
        el('td', { class: 'num', textContent: i.quantity }),
        el('td', { class: 'num', textContent: money(i.unit_price) }),
        el('td', { class: 'num', textContent: money(i.quantity * i.unit_price) })));
      box.append(el('div', { class: 'order' },
        el('h3', { textContent: 'Order #' + o.order_id + ' - ' + o.order_date + ' - ' + o.status + ' - ' + money(o.total) }),
        el('table', {},
          el('thead', {}, el('tr', {}, el('th', { textContent: 'Part' }), el('th', { class: 'num', textContent: 'Qty' }),
            el('th', { class: 'num', textContent: 'Unit' }), el('th', { class: 'num', textContent: 'Subtotal' }))),
          el('tbody', {}, ...rows))));
    });
  }

  // Init
  loadStores();
  renderOrders();
})();