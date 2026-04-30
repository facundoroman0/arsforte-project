# Plan de Refactorización: Implementación BEM y Purga de CSS

## Objetivo
Refactorizar `static/css/styles.css` (actualmente ~956 líneas) para:
1. Implementar la convención **BEM** (Block, Element, Modifier)
2. Purgar variables CSS y clases no utilizadas
3. Consolidar estilos inline de templates en el archivo principal
4. Eliminar duplicados y reducir el archivo a ~450-500 líneas

---

## Auditoría Inicial

### Estado Actual
- **Total variables CSS definidas**: 51 (en `:root`)
- **Variables no utilizadas**: 17 (33% pueden eliminarse)
- **Clases de utilidad no usadas**: ~30 (`.text-xs`, `.w-full`, etc.)
- **Reglas duplicadas**: `.glass-input:focus` definido 2 veces
- **Estilos inline**: ~300 líneas en templates que deberían moverse

### Clases Faltantes en CSS (usadas en templates pero no definidas)
- `actions-cell`, `btn-sm`, `danger-zone`, `filter-group`, `filters`, `filters-form`
- `form-card`, `form-container`, `glass-slider`, `info-row`, `inline-form`
- `loading`, `message-content`, `metric-card`, `modal-*`, `radio-group`
- `settings-container`, `settings-form`, `slider-*`, `toggle-btn`

---

## Fase 1: Purga de CSS

### 1.1 Eliminar Variables CSS No Utilizadas (`:root` líneas 1-73)

**Eliminar estas 17 variables:**
```css
--accent-cyan: rgba(93, 173, 226, 0.3);  /* No usada */
--bp-sm: 640px;
--bp-md: 768px;
--bp-lg: 1024px;
--bp-xl: 1280px;
--bp-2xl: 1536px;  /* No usadas (breakpoints hardcodeados) */
--color-accent-hover: rgba(93, 173, 226, 1);  /* No usada */
--color-border: rgba(255, 255, 255, 0.1);  /* No usada, duplicada */
--color-border-hover: rgba(255, 255, 255, 0.2);  /* No usada */
--color-primary-hover: rgba(244, 208, 63, 1);  /* No usada */
--color-secondary-hover: rgba(231, 76, 60, 1);  /* No usada */
--glass-bg-solid: #1a1a2e;  /* No usada */
--space-5: 20px;
--space-10: 40px;  /* No usadas */
--text-money: 20px;
--text-money-sm: 16px;  /* No usadas */
--transition-slow: 350ms ease;  /* No usada */
```

### 1.2 Eliminar Reglas Duplicadas

**Remover líneas 177-180** (`.glass-input:focus` duplicado, ya está en líneas 802-807)

### 1.3 Eliminar Clases No Utilizadas

| Líneas | Clase(s) | Razón |
|---------|----------|--------|
| 278 | `.text-xs` | No usada en templates |
| 283 | `.text-3xl` | No usada |
| 285 | `.font-medium` | No usada |
| 292 | `.text-accent` | No usada |
| 293 | `.text-warning` | No usada (usar `.alert-warning` en su lugar) |
| 294 | `.text-muted` | No usada |
| 297-298 | `.text-right`, `.text-left` | No usadas |
| 810-832 | `.glass-checkbox` | Python class eliminada |
| 848-850 | `.card` | No usada (usar `.glass-card`) |
| 898-904 | `.hover-scale` | No usada |
| 925-944 | `.skeleton`, `@keyframes skeleton-loading` | No usadas |
| 947-955 | `.w-full` a `.overflow-auto` | Todas no usadas |
| 785, 804, 920 | `.glass-select` standalone | No usada como clase separada |

### 1.4 Limpiar Utility Classes de Espaciado

**Mantener solo las que se usan:**
- `mt-4` (línea 577), `mt-6` (578)
- `mb-4` (579), `mb-6` (576)
- **Agregar** `mt-2`, `mb-3` (usadas en settings.html)

---

## Fase 2: Implementar Convención BEM

### Principios BEM
- **Block**: Componente independiente (`.navbar`, `.form`, `.card`, `.btn`, `.table`, `.modal`, `.alert`, `.message`, `.auth`)
- **Element**: Parte de un bloque (`.navbar__brand`, `.form__group`, `.card__header`)
- **Modifier**: Variación de bloque/elemento (`.btn--primary`, `.alert--warning`, `.card--glow-yellow`)

### Mapeo de Clases Actuales → BEM

#### 2.1 Navbar
```css
/* BEM: block = navbar */
.navbar { }                    /* era .navbar */
.navbar__content { }             /* era .navbar-content */
.navbar__brand { }              /* era .navbar-brand */
.navbar__actions { }             /* era .navbar-actions */
```

#### 2.2 Auth
```css
/* BEM: block = auth */
.auth { }                       /* era .auth-container */
.auth__card { }                 /* era .auth-card */
.auth__header { }               /* era .auth-header */
.auth__form { }                 /* era .auth-form */
.auth__footer { }               /* era .auth-footer */
.auth__btn { }                  /* era .auth-btn */
```

#### 2.3 Forms
```css
/* BEM: block = form */
.form__group { }                /* era .form-group */
.form__help { }                 /* era .form-help */
.form__error { }                /* era .form-error */
.form__actions { }              /* era .form-actions */
```

#### 2.4 Buttons
```css
/* BEM: block = btn */
.btn { }
.btn--primary { }              /* era .btn-primary */
.btn--secondary { }            /* era .btn-secondary */
.btn--danger { }              /* era .btn-danger */
.btn--ghost { }                /* era .btn-ghost */
.btn--sm { }                   /* era .btn-sm */
```

#### 2.5 Cards
```css
/* BEM: block = card */
.card { }                      /* era .glass-card */
.card--glow-yellow { }         /* era .glow-yellow */
.card--glow-cyan { }          /* era .glow-cyan */
```

#### 2.6 Table
```css
/* BEM: block = table */
.table { }
.table__head { }               /* Para th */
.table__body { }               /* Para tbody */
.table__row { }                /* Para tr */
.table__cell { }               /* Para td - opcional */
```

#### 2.7 Dashboard
```css
/* BEM: block = dashboard */
.dashboard { }
.dashboard__header { }         /* era .dashboard-header */
.dashboard__metrics { }         /* era .metrics-grid */
.dashboard__metric-card { }     /* era .metric-card */
```

#### 2.8 Alerts
```css
/* BEM: block = alert */
.alert { }
.alert--warning { }            /* era .alert-warning */
.alert__icon { }               /* era .alert-icon */
.alert__link { }               /* era .alert-link */
```

#### 2.9 Messages
```css
/* BEM: block = message */
.messages { }                  /* container */
.message { }
.message__content { }          /* era .message-content */
.message__close { }            /* era .message-close */
.message--success { }          /* era .message-success */
.message--error { }            /* era .message-error */
```

#### 2.10 Modal
```css
/* BEM: block = modal */
.modal { }                     /* overlay */
.modal__content { }
.modal__header { }
.modal__body { }
.modal__footer { }
.modal__close { }             /* era .modal-close */
```

---

## Fase 3: Mover Estilos Inline de Templates a `styles.css`

### Templates con `<style>` blocks que deben moverse:

| Template | Clases a mover | Líneas aprox. |
|----------|-----------------|---------------|
| `dashboard.html` | `.dashboard-header`, `.currency-toggle`, `.toggle-btn`, `.toggle-option`, `.rate-info`, `.metrics-grid`, `.metric-card`, `.metric-expense`, `.purchasing-power-*`, `.opportunity-grid`, `.opportunity-item`, `.apis-status`, `.api-badge`, `.api-ok`, `.api-error` | ~110 líneas |
| `settings.html` | `.settings-container`, `.settings-form`, `.slider-container`, `.slider-labels`, `.slider-value`, `.info-row`, `.danger-zone` | ~90 líneas |
| `transactions/list.html` | `.page-header`, `.filters`, `.filters-form`, `.filter-group`, `.inline-form`, `.actions-cell`, `.empty-state` | ~60 líneas |
| `transactions/form.html` | `.form-container`, `.form-card`, `.radio-group` | ~40 líneas |

**Nota**: Al mover estos estilos, aplicar la nomenclatura BEM correspondiente.

---

## Fase 4: Limpieza Final de `styles.css`

### 4.1 Estructura Final Propuesta (solo ~450-500 líneas)

```css
/* ==================== */
/* 1. VARIABLES (:root) */
/* ==================== */
:root {
  /* Solo las 34 variables que SÍ se usan */
}

/* ==================== */
/* 2. RESET & BASE */
/* ==================== */
*, *::before, *::after { }
html { }
body { }

/* ==================== */
/* 3. UTILITIES (solo las usadas) */
/* ==================== */
.text-sm, .text-base, .text-lg, .text-xl, .text-2xl { }
.font-semibold, .font-bold, .font-mono { }
.text-primary, .text-secondary, .text-secondary-text { }
.text-gain, .text-loss { }
.mt-2, .mt-4, .mt-6, .mb-3, .mb-4, .mb-6 { }

/* ==================== */
/* 4. COMPONENTS (BEM) */
/* ==================== */

/* Glass Card */
.card { }

/* Navbar */
.navbar { }
.navbar__content { }
.navbar__brand { }
.navbar__actions { }

/* Auth */
.auth { }
.auth__card { }
/* ... */

/* Buttons */
.btn { }
.btn--primary { }
/* ... */

/* Forms */
.form__group { }
.glass-input { }  /* Mantener para widget_tweaks */
/* ... */

/* Table */
.table { }
/* ... */

/* Alert */
.alert { }
/* ... */

/* Message */
.message { }
/* ... */

/* Modal */
.modal { }
/* ... */

/* Dashboard */
.dashboard { }
/* ... */

/* ==================== */
/* 5. RESPONSIVE */
/* ==================== */
@media (max-width: 768px) { }
@media (prefers-reduced-motion: reduce) { }
```

---

## Checklist de Implementación

### Fase 1: Purga (Eliminar ~300-400 líneas)
- [ ] Remover 17 variables CSS no usadas de `:root`
- [ ] Eliminar `.glass-input:focus` duplicado (líneas 177-180)
- [ ] Eliminar utility classes no usadas (`.text-xs`, `.w-full`, etc.)
- [ ] Eliminar `.glass-checkbox`, `.glass-select`, `.card`, `.hover-scale`, `.skeleton`
- [ ] Agregar `mt-2`, `mb-3` que sí se usan

### Fase 2: Refactorizar a BEM (Renombrar clases)
- [ ] **Navbar**: `.navbar-content` → `.navbar__content`, etc.
- [ ] **Auth**: `.auth-card` → `.auth__card`, etc.
- [ ] **Forms**: `.form-group` → `.form__group`, etc.
- [ ] **Buttons**: `.btn-primary` → `.btn--primary`, etc.
- [ ] **Cards**: `.glass-card` → `.card`, etc.
- [ ] **Alerts**: `.alert-warning` → `.alert--warning`, etc.
- [ ] Actualizar todos los templates con los nuevos nombres BEM

### Fase 3: Consolidar Estilos
- [ ] Mover `<style>` blocks de templates a `styles.css`
- [ ] Organizar CSS por secciones (variables, reset, utilities, components, responsive)

### Fase 4: Verificación
- [ ] Probar login/registro
- [ ] Probar dashboard
- [ ] Probar transacciones (lista, crear, editar)
- [ ] Probar settings
- [ ] Verificar responsive en móvil

---

## Estimación de Resultados

| Métrica | Antes | Después |
|----------|--------|---------|
| Líneas totales | ~956 | ~450-500 |
| Variables CSS | 51 | 34 |
| Clases definidas | ~80 | ~45 (BEM limpio) |
| Estilos inline en templates | ~300 líneas | 0 |
| Duplicados | 2-3 | 0 |

---

## Notas Importantes

1. **Orden de ejecución recomendado**:
   - Primero purgar (eliminar lo innecesario)
   - Luego refactorizar a BEM (renombrar clases)
   - Finalmente consolidar (mover estilos inline)

2. **Compatibilidad**: Mantener clases como `.glass-input` ya que se usan con `django-widget-tweaks` en los templates.

3. **Templates a actualizar con nombres BEM**:
   - `base.html`
   - `dashboard.html`
   - `settings.html`
   - `users/login.html`
   - `users/register.html`
   - `transactions/list.html`
   - `transactions/form.html`
   - `transactions/modal_detail.html`

4. **Commits recomendados**:
   - `chore: Purge unused CSS variables and classes`
   - `refactor: Implement BEM naming convention`
   - `chore: Move inline styles from templates to main CSS`
