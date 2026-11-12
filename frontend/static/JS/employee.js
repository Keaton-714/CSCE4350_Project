// Employee dashboard: order new parts, reorder, stop orders, returns
(function () {
  'use strict';

  const $ = id => document.getElementById(id);
  const money = n => '$' + Number(n).toFixed(2);

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
    toastTimer = setTimeout(() => t.hidden = true, 3000);
  }

  // Calls the backend; throws an Error with the server's message on failure.
  async function api(url, method = 'GET', body) {
    const response = await fetch(url, {
      method,
      headers: body ? { 'Content-Type': 'application/json' } : {},
      body: body ? JSON.stringify(body) : undefined
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.error || 'Something went wrong.');
    return data;
  }

  // State
  let catalog = [];     // all parts: [{part_id, name, price, category}]
  let inventory = [];   // this store's stock
  let lines = {};       // new order being built: { partId: quantity }

  const partById = id => catalog.find(p => p.part_id === +id);

  //  Tabs 
  const tabs = document.querySelectorAll('[role="tab"]');
  function showTab(tab) {
    tabs.forEach(t => {
      const selected = t === tab;
      t.setAttribute('aria-selected', selected);
      $(t.getAttribute('aria-controls')).hidden = !selected;
    });
    if (tab.id === 'tab-inventory') loadInventory();
    if (tab.id === 'tab-orders') loadOrders();
    if (tab.id === 'tab-returns') loadReturns();
  }
  tabs.forEach(t => t.addEventListener('click', () => showTab(t)));

  // Order new parts 
  async function loadCatalog() {
    catalog = await api('/api/parts');
    const select = $('new-part');
    select.replaceChildren(new Option('Choose a part', ''));
    catalog.forEach(p => select.add(new Option(`${p.name} (${money(p.price)})`, p.part_id)));
  }

  function renderLines() {
    const ids = Object.keys(lines);
    const empty = ids.length === 0;
    $('lines-empty').hidden = !empty;
    $('lines-table').hidden = empty;
    $('lines-actions').hidden = empty;

    const body = $('lines-body');
    body.replaceChildren();
    let total = 0;
    ids.forEach(id => {
      const p = partById(id);
      const qty = lines[id];
      total += p.price * qty;
      const input = el('input', { type: 'number', min: 1, value: qty });
      input.addEventListener('change', () => {
        const q = parseInt(input.value) || 0;
        if (q <= 0) delete lines[id]; else lines[id] = q;
        renderLines();
      });
      const remove = el('button', { class: 'secondary', textContent: 'Remove' });
      remove.addEventListener('click', () => { delete lines[id]; renderLines(); });
      body.append(el('tr', {},
        el('td', {}, el('strong', { textContent: p.name }), el('br'), el('span', { class: 'cat', textContent: p.category })),
        el('td', { class: 'num', textContent: money(p.price) }),
        el('td', {}, el('span', { class: 'qty' }, input)),
        el('td', { class: 'num', textContent: money(p.price * qty) }),
        el('td', {}, remove)));
    });
    $('lines-total').textContent = money(total);
  }

  $('add-line').addEventListener('click', () => {
    const id = $('new-part').value;
    const qty = parseInt($('new-qty').value);
    if (!id) return toast('Choose a part first.', true);
    if (!qty || qty < 1) return toast('Quantity must be at least 1.', true);
    lines[id] = (lines[id] || 0) + qty;
    $('new-qty').value = 1;
    renderLines();
  });

  $('clear-lines').addEventListener('click', () => { lines = {}; renderLines(); });

  $('place-order').addEventListener('click', async () => {
    const items = Object.entries(lines).map(([id, quantity]) => ({ part_id: +id, quantity }));
    try {
      const { po_id } = await api('/api/employee/orders', 'POST', { items });
      lines = {};
      renderLines();
      toast('Order #' + po_id + ' placed.');
      showTab($('tab-orders'));
    } catch (e) { toast(e.message, true); }
  });

  // Brand-new part dialog
  $('open-new-part').addEventListener('click', () => $('new-part-dialog').showModal());
  $('np-cancel').addEventListener('click', () => $('new-part-dialog').close());
  $('np-save').addEventListener('click', async () => {
    try {
      const { part_id } = await api('/api/employee/parts', 'POST', {
        name: $('np-name').value,
        category: $('np-cat').value,
        price: $('np-price').value,
        description: $('np-desc').value
      });
      await loadCatalog();
      $('new-part').value = part_id;   // preselect it so the employee can add it right away
      $('new-part-dialog').close();
      ['np-name', 'np-cat', 'np-price', 'np-desc'].forEach(id => $(id).value = '');
      toast('Part added to the catalog. Choose a quantity and add it to the order.');
    } catch (e) { toast(e.message, true); }
  });

  // Inventory 
  const LOW_STOCK = 10;

  async function loadInventory() {
    try { inventory = await api('/api/employee/inventory'); }
    catch (e) { return toast(e.message, true); }

    $('inv-empty').hidden = inventory.length > 0;
    $('inv-table').hidden = inventory.length === 0;
    const body = $('inv-body');
    body.replaceChildren();
    inventory.forEach(p => {
      const low = p.stock_quantity <= LOW_STOCK;
      const label = p.stock_quantity === 0 ? 'stock-out' : low ? 'stock-low' : 'stock-ok';
      const orderMore = el('button', { class: 'secondary', textContent: 'Order more' });
      orderMore.addEventListener('click', () => {
        $('new-part').value = p.part_id;   // preselect the part on the Order Parts tab
        $('new-qty').value = 10;
        showTab($('tab-new'));
        toast('Set the quantity and click "Add to order".');
      });
      body.append(el('tr', { class: low ? 'low-row' : '' },
        el('td', {}, el('strong', { textContent: p.name })),
        el('td', { textContent: p.category || '' }),
        el('td', { class: 'num' }, el('span', { class: label, textContent: p.stock_quantity })),
        el('td', { class: 'actions-cell' }, orderMore)));
    });
  }

  // Orders: reorder / stop / receive 
  async function loadOrders() {
    const box = $('orders');
    let orders;
    try { orders = await api('/api/employee/orders'); }
    catch (e) { return toast(e.message, true); }

    box.replaceChildren();
    if (!orders.length) { box.append(el('p', { class: 'empty', textContent: 'No orders yet.' })); return; }

    orders.forEach(o => {
      const rows = o.items.map(i => el('tr', {},
        el('td', { textContent: i.name }),
        el('td', { class: 'num', textContent: i.quantity }),
        el('td', { class: 'num', textContent: money(i.unit_cost) }),
        el('td', { class: 'num', textContent: money(i.quantity * i.unit_cost) })));

      const actions = el('div', { class: 'cart-actions' });
      const reorderBtn = el('button', { class: 'secondary', textContent: 'Reorder' });
      reorderBtn.addEventListener('click', () => act(`/api/employee/orders/${o.po_id}/reorder`, 'Order placed again.'));
      actions.append(reorderBtn);

      if (o.status === 'Pending') {
        const receiveBtn = el('button', { class: 'primary', textContent: 'Mark received' });
        receiveBtn.addEventListener('click', () => act(`/api/employee/orders/${o.po_id}/receive`, 'Stock updated.'));
        const stopBtn = el('button', { class: 'danger', textContent: 'Stop order' });
        stopBtn.addEventListener('click', () => {
          if (confirm('Stop order #' + o.po_id + '?')) act(`/api/employee/orders/${o.po_id}/stop`, 'Order stopped.');
        });
        actions.append(stopBtn, receiveBtn);
      }

      const head = el('div', { class: 'order-head' },
        el('h3', { textContent: `Order #${o.po_id} - ${o.order_date} - ${money(o.total)}` }),
        el('span', { class: 'status status-' + o.status.toLowerCase(), textContent: o.status }));

      box.append(el('div', { class: 'order' },
        head,
        o.reordered_from ? el('p', { class: 'note', textContent: 'Reorder of #' + o.reordered_from }) : '',
        el('table', {},
          el('thead', {}, el('tr', {}, el('th', { textContent: 'Part' }), el('th', { class: 'num', textContent: 'Qty' }),
            el('th', { class: 'num', textContent: 'Unit cost' }), el('th', { class: 'num', textContent: 'Subtotal' }))),
          el('tbody', {}, ...rows)),
        actions));
    });
  }

  async function act(url, message) {
    try {
      await api(url, 'POST');
      toast(message);
      loadOrders();
    } catch (e) { toast(e.message, true); }
  }

  // Returns 
  async function loadReturns() {
    try {
      inventory = await api('/api/employee/inventory');
      const history = await api('/api/employee/returns');

      const select = $('ret-part');
      select.replaceChildren(new Option('Choose a part in stock', ''));
      inventory.filter(p => p.stock_quantity > 0)
        .forEach(p => select.add(new Option(`${p.name} (${p.stock_quantity} in stock)`, p.part_id)));

      const box = $('returns');
      box.replaceChildren();
      if (!history.length) { box.append(el('p', { class: 'empty', textContent: 'No returns yet.' })); return; }
      const rows = history.map(r => el('tr', {},
        el('td', { textContent: '#' + r.return_id }),
        el('td', { textContent: r.return_date }),
        el('td', { textContent: r.name }),
        el('td', { class: 'num', textContent: r.quantity }),
        el('td', { textContent: r.reason })));
      box.append(el('table', {},
        el('thead', {}, el('tr', {}, ...['Return', 'Date', 'Part', 'Qty', 'Reason'].map(
          (h, i) => el('th', { class: i === 3 ? 'num' : '', textContent: h })))),
        el('tbody', {}, ...rows)));
    } catch (e) { toast(e.message, true); }
  }

  $('submit-return').addEventListener('click', async () => {
    try {
      await api('/api/employee/returns', 'POST', {
        part_id: $('ret-part').value,
        quantity: $('ret-qty').value,
        reason: $('ret-reason').value
      });
      $('ret-qty').value = 1;
      $('ret-reason').value = '';
      toast('Return recorded and stock updated.');
      loadReturns();
    } catch (e) { toast(e.message, true); }
  });

  //  Init 
  loadCatalog().then(renderLines).catch(e => toast(e.message, true));
})();