# Frontend Backlog: Dark Blur Glass Style

## Objetivo
Implementar un estilo visual **dark blur glass** (glassmorphism oscuro) con acentos en tonos amarillo y celeste tenues, utilizando CSS puro y Bootstrap.

## Diseño Base

### Paleta de Colores
| Token | Color | Uso |
|-------|-------|-----|
| `--glass-bg` | `#1a1a2e` (90% opacity) | Fondo de superficies de vidrio |
| `--glass-border` | `rgba(255, 255, 255, 0.1)` | Bordes translúcidos |
| `--glass-shadow` | `rgba(0, 0, 0, 0.3)` | Sombras con blur |
| `--accent-yellow` | `#f4d03f` (40% saturation) | Acentos sutiles (30% opacity) |
| `--accent-cyan` | `#5dade2` (40% saturation) | Acentos sutiles (30% opacity) |
| `--text-primary` | `rgba(255, 255, 255, 0.95)` | Texto principal |
| `--text-secondary` | `rgba(255, 255, 255, 0.6)` | Texto secundario |
| `--background-base` | `#0f0f1a` | Fondo base oscuro |
| `--blur-amount` | `12px` | Intensidad de blur |

### Estilo Glassmorphism
- Background con `backdrop-filter: blur(12px)`
- Bordes sutiles con `rgba(255, 255, 255, 0.1)`
- Sombras suaves con `0 8px 32px rgba(0, 0, 0, 0.3)`
- Gradientes sutiles en acentos

---

## Tareas

### Fase 1: Base Theme (CSS Variables & Global Styles)

- [x] **T1.1** - Definir CSS Custom Properties en `styles.css`
  - Crear variables para colors, spacing, typography
  - Implementar theme dark base
  - Fondo base: `--background-base: #0f0f1a`
  - Texto: `--text-primary`, `--text-secondary`

- [x] **T1.2** - Configurar body global y reset
  - Background oscuro uniforme
  - Typography con nueva escala
  - Evitar flash blanco en load

- [x] **T1.3** - Actualizar base.html con Bootstrap CDN
  - Agregar Bootstrap 5.3.x via CDN
  - Verificar load de estilos

### Fase 2: Componentes Glass

- [x] **T2.1** - Crear clase `.glass-card` 
  - `background: rgba(26, 26, 46, 0.7)`
  - `backdrop-filter: blur(12px)`
  - `border: 1px solid rgba(255, 255, 255, 0.1)`
  - `border-radius: 16px`
  - `box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3)`

- [x] **T2.2** - Crear clase `.glass-input`
  - Fondo translúcido
  - Borde y focus states sutiles
  - Placeholder con `--text-secondary`

- [x] **T2.3** - Estilizar botones (`.btn-glass`, `.btn-glass-primary`)
  - Glass button primario y secundario
  - Estados hover/active con glow sutil
  - Gradiente de acento amarillo/celeste

- [x] **T2.4** - Navbar glass
  - Fondo blur
  - Border inferior sutil

### Fase 3: Typography & Accents

- [x] **T3.1** - Configurar fuente
  - Font family: Inter o sistema
  - Escala tipográfica consistente

- [x] **T3.2** - Aplicar acentos
  - Color primario: `--accent-yellow` (30% opacity)
  - Color secundario: `--accent-cyan` (30% opacity)
  - Glow effects en elementos destacados

- [x] **T3.3** - Badge y tags glass
  - Tags con borde glow sutil

### Fase 4: Pages Implementation

- [x] **T4.1** - Aplicar estilo a login/register
  - Auth card glass
  - Form inputs glass
  - Botones con accent

- [x] **T4.2** - Aplicar estilo a dashboard
  - Navbar glass
  - Metric cards glass
  - Tables glass

- [x] **T4.3** - Aplicar estilo a transactions
  - List glass
  - Forms glass
  - Modal detail glass

- [x] **T4.4** - Aplicar estilo a settings
  - Configuración con cards glass

### Fase 5: Fine Tuning

- [x] **T5.1** - Messages/toasts glass
  - Notificaciones con blur y accent

- [x] **T5.2** - Responsive check
  - Verificar mobile view
  - Ajustar breakpoints si es necesario

- [x] **T5.3** - Animations
  - Transiciones suaves (150-300ms)
  - Hover effects sutiles

---

## Definition of Done

- [x] Background oscuro uniforme en toda la app
- [x] Todas las cards con efecto glass blur
- [x] Inputs con styling glass consistente
- [x] Botones con accent colors (amarillo/celeste sutil)
- [x] Responsive en mobile
- [x] No breaking changes en funcionalidad
- [x] Bootstrap integrado y funcionando

---

## Archivos a Modificar

| Archivo | Cambios |
|----------|---------|
| `static/css/styles.css` | Full rewrite con theme |
| `templates/base.html` | Agregar Bootstrap CDN |
| `templates/users/login.html` | Styling |
| `templates/users/register.html` | Styling |
| `templates/dashboard.html` | Styling |
| `templates/transactions/list.html` | Styling |
| `templates/transactions/form.html` | Styling |
| `templates/transactions/modal_detail.html` | Styling |
| `templates/settings.html` | Styling |

---

## Definition of Done

- [ ] Background oscuro uniforme en toda la app
- [ ] Todas las cards con efecto glass blur
- [ ] Inputs con styling glass consistente
- [ ] Botones con accent colors (amarillo/celeste sutil)
- [ ] Responsive en mobile
- [ ] No breaking changes en funcionalidad
- [ ] Bootstrap integrado y funcionando

---

## Notas

- Usar solo CSS puro + Bootstrap (sin SCSS/Sass)
- Mantener compatibilidad con Django template tags
- Evitar cambios en lógica de backend
- Preservar colores semánticos (income/expense)