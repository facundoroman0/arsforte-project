function openDetailModal(transactionId) {
  const modal = document.getElementById('detailModal');
  const body = document.getElementById('modalBody');
  modal.classList.add('active');
  body.innerHTML = '<div class="loading">Cargando...</div>';
  
  fetch(`/transactions/${transactionId}/detail/`)
    .then(response => response.json())
    .then(data => {
      renderAnalysis(data);
    })
    .catch(error => {
      body.innerHTML = '<p class="error">Error al cargar los datos.</p>';
    });
}

function closeModal() {
  document.getElementById('detailModal').classList.remove('active');
}

function renderAnalysis(data) {
  const body = document.getElementById('modalBody');
  const tx = data.transaction;
  const analysis = data.analysis;
  const alts = data.alternatives;
  
  const isPesos = tx.instrument === 'Pesos';
  const sign = tx.type === 'income' ? '+' : '-';
  const daysPassed = analysis.days_passed;
  
  let html = `
    <div class="transaction-info">
      <h3>${sign}$${parseFloat(tx.amount).toLocaleString('es-AR', {minimumFractionDigits: 2})} en ${tx.instrument}</h3>
      <div class="transaction-meta">
        ${tx.date} · ${tx.type === 'income' ? 'Ingreso' : 'Gasto'} · ${tx.category}
        ${tx.description ? ` · ${tx.description}` : ''}
      </div>
    </div>
  `;
  
  // Advertencia si es transacción del día
  if (daysPassed === 0) {
    html += `
      <div class="warning-note">
        ⚠️ Esta transacción es de hoy. No hay pérdida o ganancia aún. Los datos se actualizarán con el tiempo.
      </div>
    `;
  }
  
  if (isPesos && alts) {
    // Solo muestra inflación si hay días transcurridos
    if (daysPassed > 0) {
      html += `
        <div class="alternative-card">
          <div class="alternative-header">
            <span class="alternative-icon">💸</span>
            <span>Valor hoy en pesos</span>
          </div>
          <div class="alternative-values">
            <div class="alternative-value">
              <strong>$${parseFloat(analysis.value_in_pesos_today).toLocaleString('es-AR', {minimumFractionDigits: 2})}</strong>
              <span>Poder adquisitivo actual</span>
            </div>
            <div class="alternative-value">
              <strong>-${analysis.inflation_loss_pct.toFixed(1)}%</strong>
              <span>Pérdida por inflación (${daysPassed} días)</span>
            </div>
          </div>
          <div class="alternative-result loss">
            <span>Pérdida real</span>
            <span>-$${parseFloat(analysis.inflation_loss).toLocaleString('es-AR', {minimumFractionDigits: 2})}</span>
          </div>
        </div>
      `;
    }
    
    if (alts.dollar_blue) {
      const gainLoss = parseFloat(alts.dollar_blue.gain_loss);
      const gainClass = gainLoss >= 0 ? 'gain' : 'loss';
      const gainSign = gainLoss >= 0 ? '+' : '';
      const isApprox = alts.dollar_blue.details.includes('sin datos históricos');
      
      html += `
        <div class="alternative-card">
          <div class="alternative-header">
            <span class="alternative-icon">💵</span>
            <span>Si hubieras comprado dólar blue</span>
          </div>
          <div class="alternative-result ${gainClass}">
            <span>Valor hoy</span>
            <span>$${parseFloat(alts.dollar_blue.current_value).toLocaleString('es-AR', {minimumFractionDigits: 2})}</span>
          </div>
          <div style="text-align: right; margin-top: var(--space-2); font-size: var(--text-sm); color: var(--color-text-secondary);">
            ${gainSign}$${gainLoss.toLocaleString('es-AR', {minimumFractionDigits: 2})} (${gainSign}${alts.dollar_blue.percentage.toFixed(1)}%)
          </div>
          ${isApprox ? '<div class="approximate-note">* Precio del día (aproximado)</div>' : `<div class="approximate-note">${alts.dollar_blue.details}</div>`}
        </div>
      `;
    }
    
    if (alts.bitcoin) {
      const gainLoss = parseFloat(alts.bitcoin.gain_loss);
      const gainClass = gainLoss >= 0 ? 'gain' : 'loss';
      const gainSign = gainLoss >= 0 ? '+' : '';
      const isApprox = alts.bitcoin.details.includes('sin datos históricos');
      
      html += `
        <div class="alternative-card">
          <div class="alternative-header">
            <span class="alternative-icon">📈</span>
            <span>Si hubieras comprado Bitcoin</span>
          </div>
          <div class="alternative-result ${gainClass}">
            <span>Valor hoy</span>
            <span>$${parseFloat(alts.bitcoin.current_value).toLocaleString('es-AR', {minimumFractionDigits: 2})}</span>
          </div>
          <div style="text-align: right; margin-top: var(--space-2); font-size: var(--text-sm); color: var(--color-text-secondary);">
            ${gainSign}$${gainLoss.toLocaleString('es-AR', {minimumFractionDigits: 2})} (${gainSign}${alts.bitcoin.percentage.toFixed(1)}%)
          </div>
          ${isApprox ? '<div class="approximate-note">* Precio del día (aproximado)</div>' : `<div class="approximate-note">${alts.bitcoin.details}</div>`}
        </div>
      `;
    }
    
    if (alts.plazo_fijo) {
      const gainLoss = parseFloat(alts.plazo_fijo.gain_loss);
      const gainClass = gainLoss >= 0 ? 'gain' : 'loss';
      const gainSign = gainLoss >= 0 ? '+' : '';
      const isApprox = alts.plazo_fijo.details.includes('sin datos históricos');
      
      html += `
        <div class="alternative-card">
          <div class="alternative-header">
            <span class="alternative-icon">🏦</span>
            <span>Si hubieras puesto en Plazo Fijo UVA</span>
          </div>
          <div class="alternative-result ${gainClass}">
            <span>Valor hoy</span>
            <span>$${parseFloat(alts.plazo_fijo.current_value).toLocaleString('es-AR', {minimumFractionDigits: 2})}</span>
          </div>
          <div style="text-align: right; margin-top: var(--space-2); font-size: var(--text-sm); color: var(--color-text-secondary);">
            ${gainSign}$${gainLoss.toLocaleString('es-AR', {minimumFractionDigits: 2})} (${gainSign}${alts.plazo_fijo.percentage.toFixed(1)}%)
          </div>
          ${isApprox ? '<div class="approximate-note">* Precio del día (aproximado)</div>' : `<div class="approximate-note">${alts.plazo_fijo.details}</div>`}
        </div>
      `;
    }
  } else if (alts) {
    html += `
      <div class="alternative-card">
        <p style="color: var(--color-text-secondary); text-align: center;">
          Esta transacción ya está en una alternativa (${tx.instrument}).<br>
          El costo de oportunidad se calculó en relación a mantener el valor en pesos.
        </p>
      </div>
    `;
  } else {
    html += `
      <div class="alternative-card">
        <p style="color: var(--color-text-secondary); text-align: center;">
          No hay datos disponibles para calcular el costo de oportunidad.
        </p>
      </div>
    `;
  }
  
  body.innerHTML = html;
}

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    closeModal();
  }
});

document.querySelector('.modal-overlay').addEventListener('click', function(e) {
  if (e.target === this) {
    closeModal();
  }
});
