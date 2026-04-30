# Diseño UI/UX - ArsForte

## 1. Resumen Ejecutivo

Este documento describe las decisiones de diseño de interfaz para FinZap, incluyendo wireframes, paleta de colores, tipografía, y flujos de usuario. El diseño prioriza la claridad en la visualización de costos de oportunidad financieros.

---

## 2. Inventario de Pantallas

| # | Pantalla | Descripción | Prioridad |
|---|----------|-------------|-----------|
| 1 | **Dashboard** | Vista principal con métricas y costo de oportunidad | Alta |
| 2 | **Lista Transacciones** | Lista de todas las transacciones con filtros | Alta |
| 3 | **Formulario Transacción** | Modal para crear/editar transacción | Alta |
| 4 | **Login** | Inicio de sesión | Alta |
| 5 | **Registro** | Registro de nuevo usuario | Alta |
| 6 | **Configuración** | Perfil y umbral de notificaciones | Media |
| 7 | **Detalle Costo** | Modal con desglose del cálculo | Media |

---

## 3. Paleta de Colores

### 3.1 Sistema de Colores (Tokens)

| Token | Hex | RGB | Uso |
|-------|-----|-----|-----|
| `--color-primary` | `#10B981` | rgb(16, 185, 129) | Ingresos, valores positivos, CTA primario |
| `--color-primary-hover` | `#059669` | rgb(5, 150, 105) | Hover del color primario |
| `--color-secondary` | `#EF4444` | rgb(239, 68, 68) | Gastos, pérdidas, alertas |
| `--color-secondary-hover` | `#DC2626` | rgb(220, 38, 38) | Hover del color secundario |
| `--color-accent` | `#3B82F6` | rgb(59, 130, 246) | Links, acciones secundarias, Bitcoin |
| `--color-accent-hover` | `#2563EB` | rgb(37, 99, 235) | Hover del color acento |
| `--color-warning` | `#F59E0B` | rgb(245, 158, 11) | Warnings, precaución |
| `--color-background` | `#F8FAFC` | rgb(248, 250, 252) | Fondo principal de la app |
| `--color-surface` | `#FFFFFF` | rgb(255, 255, 255) | Cards, modales, superficies elevadas |
| `--color-surface-hover` | `#F1F5F9` | rgb(241, 245, 249) | Hover en superficies |
| `--color-border` | `#E2E8F0` | rgb(226, 232, 240) | Bordes, separadores |
| `--color-text-primary` | `#1E293B` | rgb(30, 41, 59) | Texto principal |
| `--color-text-secondary` | `#64748B` | rgb(100, 116, 139) | Texto secundario, labels |
| `--color-text-muted` | `#94A3B8` | rgb(148, 163, 184) | Placeholders, texto deshabilitado |

### 3.2 Significado Semántico

| Color | Significado | Uso en Contexto Financiero |
|-------|------------|---------------------------|
| Verde (`#10B981`) | Positivo | Ingresos, ganancias, balance positivo |
| Rojo (`#EF4444`) | Negativo | Gastos, pérdidas, alertas |
| Azul (`#3B82F6`) | Informativo | Links, bitcoin, información neutral |
| Amarillo (`#F59E0B`) | Advertencia | Alertas de riesgo, precaución |

### 3.3 Contraste y Accesibilidad

| Combinación | Ratio | Cumplimiento |
|-------------|-------|--------------|
| Texto oscuro sobre fondo claro | >7:1 | AAA |
| Texto secundario sobre fondo claro | >4.5:1 | AA |
| Texto blanco sobre color primario | >4.5:1 | AA |

---

## 4. Tipografía

### 4.1 Sistema de Tipografía

| Token | Valor | Uso |
|-------|-------|-----|
| `--font-sans` | `Inter, system-ui, sans-serif` | Texto general, UI |
| `--font-mono` | `'JetBrains Mono', monospace` | Montos, números, código |

### 4.2 Escala Tipográfica

| Token | Familia | Peso | Tamaño | Line-height | Uso |
|-------|---------|------|--------|-------------|-----|
| `--text-xs` | sans | 400 | 12px | 16px | Labels pequeños |
| `--text-sm` | sans | 400 | 14px | 20px | Texto secundario |
| `--text-base` | sans | 400 | 16px | 24px | Cuerpo de texto |
| `--text-lg` | sans | 500 | 18px | 28px | Subtítulos |
| `--text-xl` | sans | 600 | 20px | 28px | Títulos de sección |
| `--text-2xl` | sans | 700 | 24px | 32px | Títulos de página |
| `--text-3xl` | sans | 700 | 32px | 40px | Headlines principales |
| `--text-money` | mono | 500 | 20px | 28px | Montos grandes |
| `--text-money-sm` | mono | 500 | 16px | 24px | Montos en tablas |

---

## 5. Espaciado y Layout

### 5.1 Sistema de Espaciado

| Token | Valor | Uso |
|-------|-------|-----|
| `--space-1` | 4px | Espaciado mínimo |
| `--space-2` | 8px | Entre elementos relacionados |
| `--space-3` | 12px | Padding interno de componentes |
| `--space-4` | 16px | Padding estándar |
| `--space-5` | 20px | Gaps en layouts |
| `--space-6` | 24px | Entre secciones |
| `--space-8` | 32px | Separación de secciones mayores |
| `--space-10` | 40px | Márgenes de página |
| `--space-12` | 48px | Espaciado hero |

### 5.2 Grid y Breakpoints

| Breakpoint | Valor | Dispositivo |
|------------|-------|-------------|
| `--bp-sm` | 640px | Mobile landscape |
| `--bp-md` | 768px | Tablet |
| `--bp-lg` | 1024px | Desktop pequeño |
| `--bp-xl` | 1280px | Desktop estándar |
| `--bp-2xl` | 1536px | Desktop grande |

### 5.3 Container

```css
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-4);
}
```

---

## 6. Componentes UI

### 6.1 Botones

#### Variantes

| Variante | Uso |
|----------|-----|
| `primary` | Acciones principales (guardar, enviar) |
| `secondary` | Acciones secundarias (cancelar) |
| `danger` | Acciones destructivas (eliminar) |
| `ghost` | Acciones sin fondo (ver detalle) |

#### Estados

| Estado | Visual |
|--------|--------|
| Default | Color de variante |
| Hover | Versión más oscura (-10%) |
| Active | Versión aún más oscura (-15%) |
| Disabled | Opacidad 50%, cursor not-allowed |
| Loading | Spinner, texto "Guardando..." |

#### Especificaciones

```css
.btn {
  padding: var(--space-2) var(--space-4);
  border-radius: 8px;
  font-weight: 500;
  font-size: var(--text-sm);
  transition: all 150ms ease;
  cursor: pointer;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
}
```

### 6.2 Inputs

#### Estados

| Estado | Visual |
|--------|--------|
| Default | Border `--color-border`, bg white |
| Focus | Border `--color-accent`, ring 3px |
| Error | Border `--color-secondary`, mensaje rojo |
| Disabled | Bg `--color-surface-hover`, opacity 50% |

#### Especificaciones

```css
.input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: var(--text-base);
  transition: border-color 150ms ease;
}
.input:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
```

### 6.3 Cards

```css
.card {
  background: var(--color-surface);
  border-radius: 12px;
  padding: var(--space-6);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--color-border);
}
```

### 6.4 Badges

| Tipo | Color | Uso |
|------|-------|-----|
| Income | Verde | Ingresos |
| Expense | Rojo | Gastos |
| Warning | Amarillo | Alertas |
| Info | Azul | Información |

### 6.5 Tablas

```css
.table {
  width: 100%;
  border-collapse: collapse;
}
.table-row:nth-child(even) {
  background: var(--color-surface-hover);
}
.table-row:hover {
  background: var(--color-surface-hover);
}
```

---

## 7. Wireframes - Descripción Detallada

### 7.1 Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│ NAVBAR                                                          │
│ ┌─────────────┐                           ┌──────┐ ┌──────────┐ │
│ │ [Logo]     │                           │ 🔔  │ │ Avatar ▼ │ │
│ │ FinZap     │                           │ 2   │ └──────────┘ │
│ └─────────────┘                           └──────┘             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CARDS DE MÉTRICAS (3 columnas en desktop, 1 en mobile)         │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │ 📈 INGRESOS     │ │ 📉 GASTOS       │ │ 💰 BALANCE     │   │
│  │                 │ │                 │ │                 │   │
│  │ $500,000        │ │ $320,000        │ │ $180,000        │   │
│  │ ▲ 12% vs mes    │ │ ▼ 8% vs mes     │ │ ▲ 5% vs mes     │   │
│  │ anterior        │ │ anterior        │ │ anterior        │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
│                                                                 │
│  CARD DE COSTO DE OPORTUNIDAD                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 💸 COSTO DE OPORTUNIDAD ESTE MES                        │   │
│  │                                                          │   │
│  │  Si hubieras invertido $180,000 en:                     │   │
│  │                                                          │   │
│  │  📈 Dólar Blue        +$22,000    (+12.2%)             │   │
│  │     └── Dólar: $1,200 → $1,350                         │   │
│  │                                                          │   │
│  │  📈 Plazo Fijo UVA     +$8,000     (+4.4%)             │   │
│  │     └── Tasa: 3% mensual                                │   │
│  │                                                          │   │
│  │  📈 Bitcoin           +$45,000     (+25%)               │   │
│  │     └── BTC: $60,000 → $75,000 (ARS)                  │   │
│  │                                                          │   │
│  │  Pérdida por mantener en pesos: -$8,000               │   │
│  │                                                          │   │
│  │  [Ver cálculo detallado →]                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ALERTA DE RIESGO (solo visible si aplica)                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ⚠️ ALERTA: 70% de tu dinero está en pesos              │   │
│  │    Tu umbral configurado es 50%                        │   │
│  │    [Ajustar umbral]                                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  DISTRIBUCIÓN POR INSTRUMENTO                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Distribución actual:                                     │   │
│  │ [████████████░░░░] 70% Pesos                            │   │
│  │ [██░░░░░░░░░░░░░] 15% Plazo Fijo UVA                   │   │
│  │ [█░░░░░░░░░░░░░░] 10% Dólar Blue                       │   │
│  │ [░░░░░░░░░░░░░░░] 5% Bitcoin                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  TRANSACCIONES RECIENTES                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Fecha    │ Descripción  │ Monto      │ Instrumento │ >  │   │
│  ├──────────┼──────────────┼────────────┼────────────┼────│   │
│  │ 12/04    │ Sueldo       │ +$500,000  │ Pesos      │ >  │   │
│  │ 11/04    │ Alquiler     │ -$150,000   │ Pesos      │ >  │   │
│  │ 10/04    │ Comida       │ -$25,000    │ Dólar Blue │ >  │   │
│  │ 09/04    │ Inversión    │ +$50,000    │ UVA        │ >  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [Ver todas las transacciones →]                                │
│                                                                 │
│  [+ Nueva Transacción] (FAB button en mobile)                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Lista de Transacciones

```
┌─────────────────────────────────────────────────────────────────┐
│ TRANSACCIONES                                        [+ Nueva] │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FILTROS                                                        │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌─────────┐ │
│  │ 📅 Fecha ▼  │ │ 📁 Cat.  ▼  │ │ 💰 Inst. ▼  │ │ 🔍 Buscar│ │
│  │ Este mes    │ │ Todas       │ │ Todos       │ │         │ │
│  └──────────────┘ └──────────────┘ └──────────────┘ └─────────┘ │
│                                                                 │
│  VISTA: [Tabla ▼]  [Cards]  [Gráfico]                          │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ □  Fecha    │ Descripción   │ Cat.    │ Inst.  │ Monto  │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │ □  12/04/26 │ Sueldo        │ Sueldo  │ Pesos  │ +$500K │   │
│  │ □  11/04/26 │ Alquiler      │ Alquiler│ Pesos  │ -$150K │   │
│  │ □  10/04/26 │ Supermercado  │ Comida  │ Dólar  │ -$25K  │   │
│  │ □  09/04/26 │ Inversión     │ Inversión│ UVA   │ +$50K  │   │
│  │ □  08/04/26 │ Cena          │ Comida  │ Pesos  │ -$15K  │   │
│  │ □  07/04/26 │ Netflix       │ Servicios│ Pesos │ -$8K   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  TOTALES: Ingresos: $550,000 | Gastos: $198,000 | Balance: $352K│
│                                                                 │
│  < Página 1 de 5 >  [10 ▼] por página                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.3 Formulario Nueva Transacción

```
┌─────────────────────────────────────────────────────┐
│ Nueva Transacción                            [X]   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Tipo *                                             │
│  ┌───────────────────┐  ┌───────────────────┐       │
│  │ ● Ingreso        │  │ ○ Gasto          │       │
│  └───────────────────┘  └───────────────────┘       │
│                                                     │
│  Monto *                                            │
│  ┌───────────────────────────────────────────┐     │
│  │ $                                          │     │
│  └───────────────────────────────────────────┘     │
│                                                     │
│  Fecha *                                            │
│  ┌───────────────────────────────────────────┐     │
│  │ 📅 12/04/2026                            │     │
│  └───────────────────────────────────────────┘     │
│                                                     │
│  Categoría *                                         │
│  ┌───────────────────────────────────────────┐     │
│  │ > Seleccionar categoría...              ▼ │     │
│  └───────────────────────────────────────────┘     │
│    └─ Opciones: Sueldo, Alquiler, Comida,          │
│              Transporte, Entretenimiento,            │
│              Servicios, Inversión, Ahorro, Otro      │
│                                                     │
│  Instrumento *                                       │
│  ┌───────────────────────────────────────────┐     │
│  │ > Seleccionar instrumento...           ▼ │     │
│  └───────────────────────────────────────────┘     │
│    └─ Opciones: Pesos, Dólar Oficial, Dólar Blue,   │
│              Plazo Fijo UVA, Bitcoin                │
│                                                     │
│  Descripción                                        │
│  ┌───────────────────────────────────────────┐     │
│  │ Ej: Compra en supermercado Coto...       │     │
│  └───────────────────────────────────────────┘     │
│                                                     │
│  ┌───────────────────────────────────────────┐     │
│  │         💾 Guardar Transacción             │     │
│  └───────────────────────────────────────────┘     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 7.4 Modal Detalle Costo de Oportunidad

```
┌─────────────────────────────────────────────────────────────┐
│ Detalle: Costo de Oportunidad                        [X]   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Transacción: $100,000 en Pesos                             │
│  Fecha: 01/04/2026 (30 días)                                │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  VALOR HOY EN PESOS                                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ $92,000 en poder adquisitivo                       │    │
│  │                                                     │    │
│  │ Inflación mensual: 8%                              │    │
│  │ Perdida real: -$8,000 (-8%)                        │    │
│  │                                                     │    │
│  │ Fórmula: $100,000 × (1 - 0.08) = $92,000         │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  💵 SI HUBIERA COMPRADO DÓLAR BLUE                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Dólar el 01/04: $1,200                              │    │
│  │ Dólar hoy: $1,350                                   │    │
│  │                                                     │    │
│  │ USD comprados: 83.33                                │    │
│  │ Valor hoy: $112,500                                 │    │
│  │ Ganancia: +$12,500 (+12.5%)                        │    │
│  │                                                     │    │
│  │ Fórmula: $100,000 / $1,200 × $1,350 = $112,500    │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  📈 SI HUBIERA COMPRADO BITCOIN                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ BTC/ARS el 01/04: $60,000                          │    │
│  │ BTC/ARS hoy: $75,000                               │    │
│  │                                                     │    │
│  │ BTC comprados: 1.67                                │    │
│  │ Valor hoy: $125,250                                │    │
│  │ Ganancia: +$25,250 (+25.25%)                      │    │
│  │                                                     │    │
│  │ Fórmula: $100,000 / $60,000 × $75,000 = $125,250  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  🏦 SI HUBIERA EN PLAZO FIJO UVA                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Tasa nominal anual: 3%                             │    │
│  │ Tasa mensual: 0.25%                                │    │
│  │ UVA el 01/04: $380                                 │    │
│  │ UVA hoy: $390                                      │    │
│  │                                                     │    │
│  │ UVAs compradas: 263.16                            │    │
│  │ UVAs hoy + intereses: 263.81                      │    │
│  │ Valor hoy: $102,886                                │    │
│  │ Ganancia: +$2,886 (+2.89%)                        │    │
│  │                                                     │    │
│  │ Fórmula: (UVAs × UVA_hoy) × (1 + 0.0025)^1 = ...  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  RESUMEN                                                     │
│  │ Opción      │ Valor Actual │ vs Original │             │
│  ├─────────────┼──────────────┼─────────────┤             │
│  │ Pesos       │ $92,000      │ -8%         │  ← Perdiste  │
│  │ Plazo Fijo  │ $102,886     │ +2.9%       │             │
│  │ Dólar Blue  │ $112,500     │ +12.5%      │             │
│  │ Bitcoin     │ $125,250     │ +25.3%      │  ← Mejor opc │
│                                                             │
│                                          [Cerrar]           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7.5 Login

```
┌─────────────────────────────────────────────┐
│                                             │
│           [Logo]                            │
│          FinZap                             │
│                                             │
│     Finanzas en contexto inflacionario       │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ Email                                │    │
│  │ ██████████████████████████████████  │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ Contraseña                          │    │
│  │ ██████████████████████████████████  │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ☐ Recordarme                              │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │           Iniciar Sesión           │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ¿No tenés cuenta? [Crear una →]           │
│                                             │
└─────────────────────────────────────────────┘
```

### 7.6 Registro

```
┌─────────────────────────────────────────────┐
│                                             │
│           [Logo]                            │
│          FinZap                             │
│                                             │
│     Crear tu cuenta                        │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ Email                                │    │
│  │ ██████████████████████████████████  │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ Contraseña                          │    │
│  │ ██████████████████████████████████  │    │
│  │ Mínimo 8 caracteres                 │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ Confirmar Contraseña               │    │
│  │ ██████████████████████████████████  │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │         Crear Cuenta                │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ¿Ya tenés cuenta? [Iniciar sesión →]     │
│                                             │
└─────────────────────────────────────────────┘
```

### 7.7 Configuración

```
┌─────────────────────────────────────────────────────────────────┐
│ CONFIGURACIÓN                                      [← Volver]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PERFIL                                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Email                                                      │   │
│  │ ██████████████████████████████████████████████████████   │   │
│  │                                                             │   │
│  │ Miembro desde: 15 de enero de 2026                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  NOTIFICACIONES                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Alertas de riesgo                                         │   │
│  │                                                             │   │
│  │ Notificarme cuando el % en pesos supere:                │   │
│  │                                                             │   │
│  │  10% ────────●─────────────── 90%                       │   │
│  │                                                             │   │
│  │  Valor actual: 50%                                        │   │
│  │                                                             │   │
│  │  [ Preview: "Tenés 70% en pesos. Umbral: 50%" ]         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  EXPORTAR DATOS                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Exportar todas mis transacciones en formato JSON       │   │
│  │                                                             │   │
│  │ [Descargar mis datos]                                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ZONA PELIGRO                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Eliminar cuenta                                           │   │
│  │ Esta acción es irreversible. Se eliminarán todos tus     │   │
│  │ datos de forma permanente.                               │   │
│  │                                                             │   │
│  │ [Eliminar mi cuenta] (color rojo)                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. Flujo de Usuario

### 8.1 Mapa de Navegación

```
┌─────────────────────────────────────────────────────────────────┐
│                      ┌──────────┐                               │
│                      │ Landing   │                               │
│                      │  Login    │                               │
│                      └───┬──────┘                               │
│                          │                                       │
│              ┌───────────┴───────────┐                          │
│              │                       │                          │
│         ┌────▼────┐            ┌─────▼─────┐                    │
│         │ Registro │            │ Dashboard  │                   │
│         └─────────┘            └─────┬──────┘                    │
│                                       │                           │
│                          ┌────────────┼────────────┐              │
│                          │            │            │              │
│                    ┌─────▼─────┐ ┌───▼───┐ ┌───▼────┐           │
│                    │ Trans-    │ │Nueva  │ │Config  │           │
│                    │ acciones  │ │Transac.│ │uración │           │
│                    └─────┬─────┘ └───┬───┘ └────────┘           │
│                          │           │                           │
│                    ┌─────▼─────┐ ┌───▼────┐                     │
│                    │ Detalle   │ │ Modal  │                     │
│                    │ Costo     │ │ Form   │                     │
│                    └───────────┘ └────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 User Flows Principales

#### Flow 1: Registro e Intro

```
Usuario → Landing/Login → Click "Crear cuenta" 
→ Formulario registro → Validación 
→ Dashboard vacío → Onboarding tooltips 
→ Primera transacción
```

#### Flow 2: Agregar Transacción

```
Dashboard → Click "Nueva Transacción" 
→ Modal formulario → Llenar campos 
→ Validación → Guardar → Cerrar modal 
→ Dashboard actualizado con nueva transacción
```

#### Flow 3: Ver Detalle de Costo

```
Dashboard → Click "Ver cálculo detallado" 
→ Modal detalle → Ver desglose por instrumento 
→ Click en instrumento → Expande fórmula 
→ Cerrar modal
```

#### Flow 4: Ajustar Notificaciones

```
Dashboard → Click en alerta 
→ Link a Configuración → Slider umbral 
→ Preview actualización → Guardar 
→ Dashboard con nuevo umbral
```

---

## 9. Estados de UI

### 9.1 Estados de Carga (Loading)

| Componente | Estado Loading |
|------------|---------------|
| Dashboard | Skeleton cards con shimmer |
| Lista transacciones | Skeleton rows (5-10) |
| Formulario | Spinner en botón, inputs disabled |
| API datos | Spinner + mensaje "Actualizando..." |

### 9.2 Estados Vacíos (Empty)

| Vista | Empty State |
|-------|-------------|
| Dashboard | Ilustración + "Agregá tu primera transacción" + CTA |
| Transacciones | Ilustración + "No hay transacciones" + CTA |
| Búsqueda sin resultados | "No encontramos coincidencias" + limpiar filtros |

### 9.3 Estados de Error

| Tipo | Visual |
|------|--------|
| Error de red | Toast rojo + "No se pudo conectar. Reintentando..." |
| Error de validación | Mensaje inline debajo del input |
| Error 500 | Página de error con "Volver al inicio" |

### 9.4 Notificaciones Toast

| Tipo | Color | Duración |
|------|-------|----------|
| Éxito | Verde | 3 segundos |
| Error | Rojo | 5 segundos |
| Info | Azul | 3 segundos |
| Warning | Amarillo | 5 segundos |

---

## 10. Responsividad

### 10.1 Breakpoints

| Dispositivo | Ancho | Layout |
|-------------|-------|--------|
| Mobile | <640px | Cards apiladas, menú hamburguesa |
| Tablet | 640-1024px | Cards 2 columnas |
| Desktop | >1024px | Cards 3 columnas, sidebar |

### 10.2 Mobile Adaptations

| Componente | Desktop | Mobile |
|------------|---------|--------|
| Navbar | Horizontal | Hamburger menu |
| Cards métricas | 3 en fila | 1 columna |
| Tabla | Completa | Cards verticales |
| FAB | No | Botón flotante "+" |
| Modal | Centrado | Full screen |

### 10.3 Navegación Mobile

```
┌─────────────────────────┐
│ ☰  FinZap          🔔  │
├─────────────────────────┤
│                         │
│   [Dashboard cards]     │
│                         │
│   [Content]             │
│                         │
│                         │
│                    [+]  │
│                         │
├─────────────────────────┤
│ 🏠    📊    ⚙️          │
│ Home  Trans.  Config    │
└─────────────────────────┘
```

---

## 11. Accesibilidad

### 11.1 Requisitos WCAG 2.1 AA

| Requisito | Implementación |
|-----------|----------------|
| Contraste | Ratio mínimo 4.5:1 para texto |
| Focus visible | Outline 2px en focus |
| Labels | Todos los inputs con `<label>` |
| Alt text | Imágenes con alt descriptivo |
| Keyboard nav | Tab, Enter, Escape funcionales |

### 11.2 Áreas de Mejora Futura

| Área | Descripción |
|------|-------------|
| Screen reader | Aria labels completos |
| Skip links | Link para saltar al contenido |
| High contrast | Modo alto contraste |
| Reduced motion | Desactivar animaciones |

---

## 12. Componentes por Página

| Pantalla | Componentes |
|----------|-------------|
| Dashboard | Navbar, MetricCard (x3), OpportunityCard, AlertCard, DistributionBar, TransactionList, FAB |
| Transacciones | Navbar, FilterBar, TransactionTable, Pagination, FAB |
| Formulario | Modal, RadioGroup, Input, Select, Textarea, Button |
| Login/Registro | Form, Input, Button, Link |
| Configuración | Navbar, SettingsSection, Slider, DangerZone |
| Detalle Costo | Modal, BreakdownCard (x4), SummaryTable |

---

## 13. Próximos Pasos

1. [ ] Revisar y validar wireframes con stakeholders
2. [ ] Ajustar basándose en feedback
3. [ ] Crear prototype interactivo en Figma
4. [ ] Definir animaciones y transiciones
5. [ ] Generar assets (íconos, ilustraciones empty state)

---

## 14. Diseño Dark Glass (Actual)

A partir de abril 2026, el diseño evolucionó hacia un estilo Dark Glass con glassmorphism, manteniendo la identidad visual pero con un aspecto más moderno y sofisticado.

### 14.1 Nueva Paleta de Colores

| Token | Hex | Uso |
|-------|-----|-----|
| `--color-cyan` | `#34D1BF` | Acento principal, branding |
| `--color-orange` | `#FFA62B` | Acento secundario, advertencias |
| `--color-positive` | `#10b981` | Ingresos, valores positivos |
| `--color-negative` | `#e74c3c` | Gastos, pérdidas, errores |
| `--bg-base` | `#0c0c0f` | Fondo principal |
| `--bg-secondary` | `#161618` | Fondo secundario |

### 14.2 Sistema Glass

```css
:root {
  --glass-bg: rgba(24, 24, 28, 0.7);
  --glass-border: rgba(255, 255, 255, 0.05);
  --glass-blur: 10px;
}

.glass {
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
}
```

### 14.3 Badges de Cristal

| Badge | Estilo |
|-------|--------|
| `.badge-glass-success` | Verde: bg rgba(16,185,129,0.25), border rgba(16,185,129,0.4) |
| `.badge-glass-danger` | Rojo: bg rgba(231,76,60,0.25), border rgba(231,76,60,0.4) |
| `.badge-glass-warning` | Naranja: bg rgba(255,166,43,0.25), border rgba(255,166,43,0.4) |
| `.badge-glass` | Base: border-radius 50px, padding 0.35em 0.65em |

### 14.4 Componentes Actualizados

- **Navbar**: Fondo sólido #121214 con border-bottom sutil (rgba 0.08)
- **Cards**: Clase `.glass` con border-radius 12px
- **Modales**: Contenido glass con border-radius 12px
- **Formularios**: Inputs con clase `.glass` y estilos enfocados en cyan
- **Tablas**: Estilos glass con bordes sutiles y hover

### 14.5 Tipografía

- **Font Mono**: JetBrains Mono, Fira Code (para montos)
- **Textos**: Inter, system-ui, sans-serif

### 14.6 Archivo CSS

| Archivo | Estado |
|---------|--------|
| `global-styles.css` | **Activo** - contiene todos los estilos unificados |
| `styles.css` | Eliminado |
| `styles-refactored.css` | Eliminado |
| `bootstrap-custom.css` | Eliminado |

---

## 15. Próximos Pasos

1. [ ] Documentar cambios en próximas iteraciones
2. [ ] Actualizar wireframes al nuevo diseño
3. [ ] Agregar más variantes de badges
4. [ ] Implementar animaciones smooth

---

*Documento generado usando ui-ux-designer skill*
*Fecha: 2026-04-30*
