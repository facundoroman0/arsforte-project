# Plan de Implementación - ArsForte

## Sprint 1: Setup y Estructura ✓

- [x] Inicializar proyecto Django
- [x] Configurar settings (SQLite, timezone AR, apps)
- [x] Crear estructura de templates/static
- [x] Configurar pytest para tests

## Sprint 2: Autenticación ✓

- [x] Custom User model con email como PK
- [x] Registro de usuarios
- [x] Login/Logout con Django auth
- [x] Tests de autenticación

## Sprint 3: Modelos y Migraciones ✓

- [x] Modelo Transaction
- [x] Choices para categorías e instrumentos
- [x] Migraciones
- [x] Índices (user_id, date)

## Sprint 4: CRUD Transacciones ✓

- [x] Lista de transacciones con filtros
- [x] Create transaction (form + view)
- [x] Edit/Delete transactions
- [x] Validaciones

## Sprint 5: Dashboard y Métricas ✓

- [x] Cards: ingresos, gastos, balance
- [x] Query de agregación por instrumento
- [x] Distribución visual (% por instrumento)

## Sprint 6: APIs Externas ✓

- [x] Servicio Bluelytics (dólar blue)
- [x] Servicio CoinGecko (Bitcoin)
- [x] Servicio Inflación (fuente a definir)
- [x] Servicio BCRA (tasas UVA)
- [x] Cache con TTL 15min

## Sprint 7: Cálculos Costo de Oportunidad ✓

- [x] Función: valor actual vs dólar blue
- [x] Función: valor actual vs plazo fijo UVA
- [x] Función: valor actual vs Bitcoin
- [x] Función: pérdida por inflación
- [x] Modal detalle por transacción

## Sprint 8: Notificaciones y Configuración ✓

- [x] Alertas cuando % pesos > umbral
- [x] Settings: ajustar umbral
- [x] Tests de notificaciones

## Sprint 9: Polish UI/UX ✓

- [x] Empty states
- [x] Manejo de errores graceful
- [x] Tests integración
- [x] Validación de cálculos

## Sprint 10: Refactorización UI (Dark Glass) ✓

- [x] Migración a diseño dark glass/glassmorphism
- [x] Unificación de CSS en global-styles.css
- [x] Badges con estilos de cristal redondeados (badge-glass)
- [x] Formularios con estilos glass (login, register, transactions)
- [x] Optimización de templates con extra_css/extra_js
- [x] Fix de botones y формы
- [x] Fix de detalles en modal de transacción

## Sprint 11: Optimizaciones de Rendimiento ✓

- [x] Cache a nivel dashboard
- [x] Invalidación de cache
- [x] Optimización de queries de transacciones
- [x] Bug fixes varios

---

## Histórico de Cambios (Changelog)

### v1.0 - Latest (2026-04-30)

#### UI/UX
- Nuevo diseño Dark Glass con glassmorphism
- Paleta: cyan (#34D1BF), orange (#FFA62B), negativo (#e74c3c), positivo (#10b981)
- Background: gradiente oscuro (#0c0c0f → #161618)
- Clase `.glass` reutilizable con backdrop-filter
- Badges redondeados (badge-glass-success, badge-glass-danger, badge-glass-warning)
- Formularios con estilos glass (clase .glass en inputs)
- Navbar con fondo sólido y divider sutil

#### CSS
- Unificación: styles.css y styles-refactored.css eliminados
- Nuevo archivo: global-styles.css
- Separación de estilos por template (extra_css/extra_js)
- Bootstrap personalizado sin conflictos

#### Funcionalidad
- Formularios de login/register con email como username
- Modal de detalles de transacción mejorado
- Cache de dashboard con invalidación
- Optimización de queries de transacciones

#### Bug Fixes
- Fix radius badges
- Fix forms transaction
- Fix issues on details
- Fix login and register forms
- Fix details modal (JS inline code removed)
- Fix light buttons
- Fix buttons
- Fix api status badges
- Fix bg cards
