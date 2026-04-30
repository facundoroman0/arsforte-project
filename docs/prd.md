# PRD: ArsForte - Finanzas Personales en Contexto Inflacionario

## 1. Introducción / Resumen

ArsForte es una aplicación web de finanzas personales diseñada específicamente para el contexto argentino, donde mantener dinero en pesos significa perder poder adquisitivo de forma constante. A diferencia de las apps de finanzas genéricas (Mint, YNAB), ArsForte integra datos de inflación, dólar blue, plazo fijo UVA y criptomonedas para mostrar al usuario el verdadero costo de sus decisiones financieras.

El problema que resuelve: la mayoría de las apps de finanzas solo muestran "cuánto gastaste". ArsForte muestra "cuánto te costaron tus decisiones financieras" al comparar el rendimiento real del dinero en pesos contra alternativas como dólar, plazo fijo UVA o bitcoin.

## 2. Objetivos

- Permitir al usuario registrar ingresos y gastos con información de dónde tuvo guardado ese dinero (pesos, dólar, plazo fijo UVA)
- Consumir APIs externas en tiempo real para obtener: inflación acumulada (INDEC), cotización dólar blue (bluelytics.com.ar), tasas de plazo fijo (BCRA), precio de bitcoin
- Calcular el valor real de cada decisión financiera comparando el monto original contra qué habría rendido invertido en alternativas
- Mostrar en un dashboard el "costo de oportunidad" de las decisiones financieras del usuario
- Proporcionar notificaciones internas cuando el usuario está perdiendo poder adquisitivo significativo
- Soportar múltiples usuarios con registro y autenticación

## 3. Historias de Usuario

- **Como usuario argentino quiero** registrar mis transacciones indicando en qué instrumento tenía guardado ese dinero, **para que** la app pueda calcular cuánto perdió o ganó en términos reales.

- **Como usuario quiero** ver un dashboard que me muestre el costo de mis decisiones financieras este mes, **para** entender qué tan bien estoy administrando mi dinero vs otras alternativas.

- **Como usuario quiero** recibir notificaciones internas cuando mi dinero en pesos está perdiendo demasiado valor real, **para** tomar acción a tiempo.

- **Como usuario nuevo quiero** registrarme fácilmente en la app, **para** empezar a rastrear mis finanzas inmediatamente.

- **Como usuario quiero** categorizar mis transacciones (sueldo, alquiler, comida, etc.), **para** entender en qué estoy gastando y dónde tengo guardado mi dinero.

## 4. Requerimientos Funcionales

### 4.1 Autenticación y Usuarios

1. El sistema debe permitir el registro de nuevos usuarios con email y contraseña
2. El sistema debe permitir el inicio de sesión con email y contraseña
3. El sistema debe mantener sesiones de usuario activas
4. Cada usuario debe tener acceso solo a sus propios datos

### 4.2 Gestión de Transacciones

5. El usuario debe poder crear una transacción con: fecha, monto, categoría, y tipo de instrumento donde tenía el dinero
6. Las categorías disponibles deben incluir: sueldo, alquiler, comida, transporte, entretenimiento, servicios, inversión, ahorro, otro
7. Los tipos de instrumento disponibles deben incluir: pesos, dólar (oficial), dólar blue, plazo fijo UVA, bitcoin
8. El usuario debe poder visualizar sus transacciones en una lista ordenada por fecha
9. El usuario debe poder editar una transacción existente
10. El usuario debe poder eliminar una transacción existente

### 4.3 Consumo de APIs Externas

11. El sistema debe consumir la API de bluelytics.com.ar para obtener la cotización del dólar blue actualizada
12. El sistema debe obtener datos de inflación acumulada desde una fuente pública (INDEC o similar)
13. El sistema debe obtener tasas de plazo fijo desde datos públicos del BCRA
14. El sistema debe obtener el precio actual de bitcoin desde una API pública
15. Los datos externos deben actualizarse en tiempo real (al momento de consultar el dashboard)
16. El sistema debe manejar gracefulmente errores cuando las APIs externas no estén disponibles

### 4.4 Cálculo de Valor Real

17. El sistema debe calcular cuánto habría rendido cada monto si se hubiera invertido en dólar blue desde la fecha de la transacción
18. El sistema debe calcular cuánto habría rendido cada monto si se hubiera invertido en plazo fijo UVA desde la fecha de la transacción
19. El sistema debe calcular cuánto habría rendido cada monto si se hubiera invertido en bitcoin desde la fecha de la transacción
20. El sistema debe comparar el valor actual en pesos contra las alternativas y mostrar la diferencia
21. El cálculo debe considerar la inflación acumulada desde la fecha de cada transacción

### 4.5 Dashboard

22. El dashboard debe mostrar el total de ingresos y gastos del usuario
23. El dashboard debe mostrar el "costo de oportunidad" total: cuánto perdió o ganó en términos reales por no invertir mejor
24. El dashboard debe desglosar el costo por tipo de instrumento (cuánto perdió por tener en pesos vs otras opciones)
25. El dashboard debe mostrar un resumen visual del patrimonio actual
26. Los datos del dashboard deben actualizarse en tiempo real al visitar la página

### 4.6 Notificaciones

27. El sistema debe mostrar notificaciones internas cuando el usuario tenga más del 50% de su dinero en pesos
28. El sistema debe mostrar notificaciones internas cuando el costo de oportunidad supere un umbral configurable
29. Las notificaciones deben ser visibles en el dashboard

### 4.7 Categorías y Reportes

30. El sistema debe mostrar un desglose de gastos por categoría
31. El usuario debe poder filtrar transacciones por rango de fechas

## 5. No Objetivos (Fuera de Alcance)

- No se implementará importación de transacciones desde archivos CSV o APIs de bancos en esta versión
- No se implementarán proyecciones futuras o análisis predictivo
- No se enviarán notificaciones por email, solo internas dentro de la app
- No se integrará con billeteras virtuales específicas (Mercado Pago, etc.)
- No se implementará exportación de datos a PDF o Excel
- No se implementará soporte para múltiples monedas en una sola transacción
- No se manejarán inversiones en criptomonedas más allá de bitcoin

## 6. Consideraciones de Diseño

Por definir en iteración posterior. Se usará un diseño simple con HTML/CSS vanilla:

- Dashboard principal con cards para cada métrica
- Lista de transacciones reciente
- Formulario para agregar nueva transacción
- Barra de navegación simple

## 7. Consideraciones Técnicas

### Stack Tecnológico

- **Backend:** Python con Django
- **Base de datos:** SQLite
- **Frontend:** Django Templates (HTML/CSS) + Vanilla JavaScript para interactividad básica
- **APIs externas:** bluelytics.com.ar (dólar blue), INDEC (inflación), BCRA (tasas plazo fijo), CoinGecko (bitcoin)

### Estructura de Base de Datos

- Tabla `users`: id, email, password_hash, created_at
- Tabla `transactions`: id, user_id, date, amount, category, instrument_type, description, created_at

### Integraciones Requeridas

- API de bluelytics.com.ar para cotización dólar blue
- Datos de inflación INDEC (considerar web scraping o API alternativa si no hay API oficial)
- Tasas de interés del BCRA para plazo fijo UVA
- API de CoinGecko para precio de bitcoin

## 8. Métricas de Éxito

- Usuario puede registrarse e iniciar sesión correctamente
- Usuario puede agregar, editar y eliminar transacciones
- Dashboard muestra datos actualizados en tiempo real
- Cálculos de costo de oportunidad son exactos dentro del 1% de diferencia
- Notificaciones se muestran cuando corresponde
- La app es usable por usuarios sin conocimiento financiero previo

## 9. Preguntas Abiertas

1. ¿Cuál es el formato exacto de los datos de inflación del INDEC? ¿Hay una API o será necesario web scraping?
2. ¿El usuario puede configurar el umbral de notificaciones o debe ser fijo?
3. ¿Se requiere histórico de transacciones o solo el estado actual?
4. ¿Para el cálculo de plazo fijo UVA, se debe considerar la evolución del capital por intereses compuestos?
5. ¿El usuario puede ver el detalle de cómo se calculó cada costo de oportunidad?

---

## 10. Decisiones Tomadas

### 10.1 Fuente de Datos de Inflación

**Decisión: Usar API alternativa en vez de web scraping**

| Opción | Selección |
|--------|-----------|
| Web scraping INDEC | Descartado - frágil, puede cambiar estructura |
| API BCRA | No tiene IPC exacto |
| API alternativa (ej: indicadoresdeldia.com) | **Seleccionado** - confiable y fácil |

**Implementación:** Consumir API de terceros que ya tenga el IPC mensual parseado. Si la API no está disponible, usar web scraping como fallback con cache largo (1 día).

---

### 10.2 Umbral de Notificaciones

**Decisión: Configurable por el usuario, valor por defecto 50%**

| Perfil | Umbral sugerido |
|--------|----------------|
| Conservador | 30% en pesos |
| Normal | 50% (default) |
| Agresivo | 70% en pesos |

**Implementación:**
- Campo `notification_threshold` en tabla `users` (ya incluido en schema)
- Rango válido: 10% - 90%
- UI: Slider en sección de settings
- Default: 50%

---

### 10.3 Histórico de Transacciones

**Decisión: Solo estado actual, no auditoría completa**

| Consideración | Análisis |
|--------------|----------|
| Usuario típico | Edita/corrige errores, no necesita historial |
| Complejidad | Mantener histórico ralentiza queries |
| Auditoría | Solo `updated_at` para saber cuándo se modificó |

**Implementación:**
- Tabla `transactions` solo tiene estado actual
- Campo `updated_at` registra última modificación
- En v2: evaluar agregar `transaction_history` si hay demanda

---

### 10.4 Cálculo de Plazo Fijo UVA

**Decisión: Usar interés compuesto**

**Fórmula:**
```
capital_final = capital_inicial × (1 + tasa_mensual)^meses
```

| Parámetro | Fuente |
|-----------|--------|
| UVA actual | API BCRA |
| Tasa nominal anual | BCRA (~3% en 2026) |
| Plazo mínimo | 30 días |
| Capitalización | Mensual (compuesta) |

**Implementación:**
- Calcular usando fórmula de interés compuesto
- Asumir reinversión automática del capital
- Mostrar desglose: capital original + intereses + ajuste UVA

---

### 10.5 Detalle del Cálculo de Costo de Oportunidad

**Decisión: Sí, mostrar desglose completo al usuario**

**UI propuesta:**

```
💸 Transacción: $100,000 en pesos (01/04/2026)
├── Valor hoy: $92,000 en poder adquisitivo
│   └── Inflación: 8% en 30 días
├── Si hubiera comprado dólar blue: $108,000
│   └── Dólar subió de $1,200 a $1,350 (+12.5%)
└── Si hubiera comprado Bitcoin: $125,000
    └── BTC subió 25% vs ARS
```

**Implementación:**
- Expandir en tooltip o modal
- Mostrar fórmula explícita
- Educar al usuario sobre conceptos financieros
- Comparar: pesos vs dólar blue vs plazo fijo UVA vs bitcoin

---

*Documento generado para ArsForte - Finanzas Personales en Contexto Inflacionario*
*Última actualización: 2026-04-22*
