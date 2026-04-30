# Diseño de Base de Datos - ArsForte

## 1. Resumen Ejecutivo

Este documento describe el diseño de la capa de datos para FinZap, una aplicación de finanzas personales enfocada en el contexto inflacionario argentino. El diseño prioriza la simplicidad para la fase inicial, con compatibilidad dual SQLite (desarrollo) y PostgreSQL (producción).

---

## 2. Requerimientos de Datos (del PRD)

### 2.1 Entidades Principales

| Entidad | Descripción | Operaciones principales |
|---------|-------------|------------------------|
| `users` | Usuarios registrados en la plataforma | Registro, login, gestión de preferencias |
| `transactions` | Transacciones financieras del usuario | CRUD, filtrado, agregación |

### 2.2 Categorías de Transacciones (enum)

```
sueldo, alquiler, comida, transporte, entretenimiento, 
servicios, inversión, ahorro, otro
```

### 2.3 Tipos de Instrumento Financiero (enum)

```
pesos, dolar_oficial, dolar_blue, plazo_fijo_uva, bitcoin
```

### 2.4 APIs Externas a Consumir

| API | Datos | Uso |
|-----|-------|-----|
| bluelytics.com.ar | Cotización dólar blue | Cálculo de costo de oportunidad |
| CoinGecko | Precio Bitcoin/USD | Cálculo de costo de oportunidad |
| INDEC/BCRA | Inflación acumulada, tasas UVA | Cálculo de valor real |
| BCRA | Tasas plazo fijo UVA | Cálculo de proyecciones |

---

## 3. Modelo de Datos

### 3.1 Diagrama Entidad-Relación (ERD)

```mermaid
erDiagram
    USERS {
        uuid id PK
        string email UK
        string password_hash
        decimal notification_threshold
        timestamp created_at
        timestamp updated_at
    }
    
    TRANSACTIONS {
        uuid id PK
        uuid user_id FK
        date date
        decimal amount
        string transaction_type
        string category
        string instrument_type
        text description
        timestamp created_at
        timestamp updated_at
    }
    
    USERS ||--o{ TRANSACTIONS : "has"

    USERS {
        note: "1 usuario tiene N transacciones"
    }
```

### 3.2 Tabla: `users`

| Campo | Tipo | Constraints | Descripción |
|-------|------|------------|-------------|
| `id` | UUID | PK, DEFAULT | Identificador único |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | Email del usuario |
| `password_hash` | VARCHAR(255) | NOT NULL | Hash bcrypt de la contraseña |
| `notification_threshold` | DECIMAL(5,2) | DEFAULT 50.00 | Umbral de notificación (%) |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Fecha de creación |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Última modificación |

**Decisiones de diseño:**
- `notification_threshold`: Permite al usuario configurar el % máximo de pesos antes de recibir alertas. Valor por defecto 50%.
- `updated_at`: Para auditoría y cache invalidation.

### 3.3 Tabla: `transactions`

| Campo | Tipo | Constraints | Descripción |
|-------|------|------------|-------------|
| `id` | UUID | PK, DEFAULT | Identificador único |
| `user_id` | UUID | FK → users.id, NOT NULL | Propietario de la transacción |
| `date` | DATE | NOT NULL | Fecha de la transacción |
| `amount` | DECIMAL(15,2) | NOT NULL | Monto (siempre positivo) |
| `transaction_type` | VARCHAR(10) | NOT NULL, CHECK | 'income' o 'expense' |
| `category` | VARCHAR(50) | NOT NULL | Categoría de la transacción |
| `instrument_type` | VARCHAR(30) | NOT NULL | Instrumento financiero |
| `description` | TEXT | NULLABLE | Descripción opcional |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Fecha de creación |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Última modificación |

**Decisiones de diseño:**
- `amount` siempre positivo: el signo se define en `transaction_type` ('income'/'expense'). Esto simplifica los cálculos de agregación.
- `DECIMAL(15,2)`: Soporta montos hasta 999.999.999.999,99 - suficiente para la mayoría de casos de uso.
- `user_id` con CASCADE DELETE: al eliminar un usuario se eliminan sus transacciones.

---

## 4. Índices

### 4.1 Estrategia de Indexado

| Índice | Columnas | Tipo | Justificación |
|--------|----------|------|---------------|
| `idx_transactions_user_date` | (user_id, date DESC) | B-tree | Listado principal: transacciones por usuario ordenadas por fecha |
| `idx_transactions_user_category` | (user_id, category) | B-tree | Filtrado por categoría en dashboard |
| `idx_transactions_user_instrument` | (user_id, instrument_type) | B-tree | Filtrado por instrumento para cálculo de costo de oportunidad |
| `idx_users_email` | (email) | B-tree | Búsqueda para login |

### 4.2 Índices Partial (PostgreSQL)

```sql
-- Para dashboard mensual (optimización futura)
CREATE INDEX idx_transactions_user_date_month 
ON transactions(user_id, date DESC) 
WHERE date >= CURRENT_DATE - INTERVAL '12 months';
```

---

## 5. Normalización

### 5.1 Forma Normal

| Tabla | 1NF | 2NF | 3NF |
|-------|-----|-----|-----|
| `users` | ✓ | ✓ | ✓ |
| `transactions` | ✓ | ✓ | ✓ |

**Decisión:** Las categorías e instrumentos no se extraen a tablas separadas porque:
1. Son enums cerrados (no crece dinámicamente)
2. La complejidad de JOIN no justifica el cambio
3. Simplifica el frontend (dropdowns hardcodeados)

### 5.2 Desnormalización Opcional (Fase 2)

Para optimizar el dashboard, considerar:

```sql
-- Vista materializada para resumen mensual
CREATE MATERIALIZED VIEW monthly_summary AS
SELECT 
    user_id,
    DATE_TRUNC('month', date) as month,
    transaction_type,
    instrument_type,
    SUM(amount) as total,
    COUNT(*) as count
FROM transactions
GROUP BY user_id, month, transaction_type, instrument_type;
```

---

## 6. Seguridad

### 6.1 Contraseñas

- Algoritmo: **bcrypt** con cost factor 12
- Almacenamiento: solo el hash, nunca la contraseña en texto plano
- Longitud mínima: 8 caracteres

### 6.2 Aislamiento de Datos

- Cada query de transacciones filtra por `user_id`
- El `user_id` se extrae del token de sesión, nunca del request
- Row-Level Security (RLS) en PostgreSQL para producción

### 6.3 SQL Injection

- Todos los inputs parametrizados via ORM/Django
- Validación de tipos en la capa de aplicación

---

## 7. Compatibilidad SQLite / PostgreSQL

### 7.1 Tipos de Datos

| Concepto | SQLite | PostgreSQL |
|---------|--------|------------|
| UUID | TEXT | UUID |
| Timestamp | TEXT (ISO8601) | TIMESTAMP |
| Decimal | REAL | DECIMAL(15,2) |
| Fecha | TEXT (YYYY-MM-DD) | DATE |

### 7.2 Implementación Recomendada

Usar **Django ORM** que abstrae las diferencias automáticamente:

```python
from django.db import models
import uuid

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Django maneja SQLite/PostgreSQL automáticamente
```

### 7.3 Migraciones

| Herramienta | Justificación |
|------------|---------------|
| **Django Migrations** | Integrado en Django, migrations versionadas |

---

## 8. Cálculo de Costo de Oportunidad (Persistencia)

### 8.1 Datos de APIs Externas

Los datos de APIs externas (dólar, bitcoin, inflación) **NO se persisten**. Se consumen en tiempo real para:
- Evitar datos obsoletos
- Simplificar la arquitectura
- No depender de scheduled jobs

### 8.2 Histórico de Cotizaciones (Fase 2)

Si se requiere histórico de cotizaciones:

```sql
CREATE TABLE exchange_rates (
    id UUID PRIMARY KEY,
    currency_pair VARCHAR(20) NOT NULL,
    rate DECIMAL(15,4) NOT NULL,
    fetched_at TIMESTAMP NOT NULL,
    UNIQUE(currency_pair, fetched_at)
);
```

---

## 9. Volumen de Datos Estimado

| Métrica | Estimación |
|---------|------------|
| Usuarios | 1,000 - 100,000 |
| Transacciones/usuario/mes | ~50-100 |
| Tamaño promedio por transacción | ~150 bytes |
| Crecimiento anual | ~20% |

**Proyección:**
- 1,000 usuarios × 100 tx × 12 meses × 150 bytes = ~180 MB/año
- 100,000 usuarios × 100 tx × 12 meses × 150 bytes = ~18 GB/año

**Conclusión:** SQLite es viable hasta ~10,000 usuarios. PostgreSQL recomendado desde 10,000+.

---

## 10. Decisiones de Diseño Resumen

| Decisión | Alternativas | Selección |
|----------|--------------|-----------|
| UUID vs autoincrement | UUID, BIGINT | **UUID** (distribuido, seguro) |
| Foreign keys | ON DELETE CASCADE, SET NULL | **CASCADE** (usuario elimina = datos eliminados) |
| Timestamps | Solo created_at, ambos | **Ambos** (auditoría completa) |
| Índices compuestos | Múltiples idx simples | **Idx compuestos** (queries frecuentes) |
| Categories/Enums | Tabla separada, enum DB, string | **String** (enum cerrado, simple) |
| ORM | Django ORM | **Django ORM** (Python + Django) |

---

## 11. Próximos Pasos

1. [ ] Generar migraciones con Django migrations
2. [ ] Definir modelos Django
3. [ ] Crear seed data para testing
4. [ ] Implementar vistas y formularios
5. [ ] Escribir tests unitarios

---

## 12. Decisiones Adicionales (Contextuales)

### 12.1 Auditoría de Cambios en Transacciones

**Decisión: NO para MVP, `updated_at` sí**

| Consideración | Análisis |
|--------------|----------|
| Complejidad | Agregar histórico multiplica las queries |
| Usuario típico | Arregla errores puntual, no necesita historial |
| Costo/beneficio | Alto esfuerzo, bajo valor inicial |

**Implementación actual:** `updated_at` registra última modificación. En v2 evaluar agregar `transaction_history`.

---

### 12.2 Cache de Cotizaciones (Inflation/Exchange Rates)

**Decisión: SÍ, con TTL de 15 minutos**

| Consideración | Análisis |
|--------------|----------|
| APIs externas | Bluelytics, CoinGecko pueden fallar o tardar |
| Cálculos | Requieren datos de fecha de transacción + actuales |
| Offline | Si usuario consulta sin internet, falla |

**Schema propuesto:**

```sql
CREATE TABLE exchange_rate_cache (
    source VARCHAR(20) PRIMARY KEY,
    data JSONB NOT NULL,
    fetched_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL
);
```

**Estrategia:**
- TTL: 15 minutos para dólar/bitcoin/inflación
- Si falla API: usar cache aunque esté vencido (graceful degradation)
- Invalidación manual si datos parecen incorrectos

---

### 12.3 Límite de Transacciones por Usuario

**Decisión: Sin límite artificial**

| Consideración | Análisis |
|--------------|----------|
| Storage | 100k transacciones ≈ 15 MB |
| Índices | Ya optimizados para alto volumen |
| UX | Limitar genera frustración |

**Límites prácticos:**
- SQLite: funcional hasta ~10k usuarios
- PostgreSQL: ilimitado

---

### 12.4 Exportación de Datos del Usuario

**Decisión: SÍ, JSON básico**

| Consideración | Análisis |
|--------------|----------|
| Regulación AR | LDA (Ley de Datos Personales) sugiere portabilidad |
| UX | Confianza del usuario en sus datos |
| Complejidad | Bajo esfuerzo con schema simple |

**Endpoint propuesto:**

```
GET /api/export
```

**Respuesta:**
```json
{
  "user": {
    "email": "user@example.com",
    "created_at": "2026-01-01T00:00:00Z"
  },
  "transactions": [
    {
      "id": "uuid",
      "date": "2026-04-01",
      "amount": 50000.00,
      "transaction_type": "income",
      "category": "sueldo",
      "instrument_type": "pesos",
      "description": "Salario abril"
    }
  ],
  "exported_at": "2026-04-13T22:00:00Z"
}
```

---

## 13. Próximos Pasos

1. [ ] Generar migraciones con Django migrations
2. [ ] Definir modelos Django
3. [ ] Crear tabla `exchange_rate_cache`
4. [ ] Crear seed data para testing
5. [ ] Implementar vistas y formularios
6. [ ] Implementar vista de export
7. [ ] Escribir tests unitarios

---

## 14. Resumen de Decisiones

| Aspecto | Decisión | Justificación |
|---------|----------|---------------|
| Auditoría cambios | No MVP | Alto esfuerzo, bajo valor |
| Cache cotizaciones | Sí, TTL 15min | Graceful degradation |
| Límite transacciones | Sin límite | Experiencia de usuario |
| Export datos | Sí, JSON | Compliance + confianza |
| UUID vs BIGINT | UUID | Seguro y distribuido |
| Foreign keys | CASCADE | Simplifica cleanup |
| Índices | Compuestos | Queries frecuentes optimizadas |
| ORM | Django ORM | Abstracción multi-DB nativa |

---

*Documento generado usando database-architect skill*
*Fecha: 2026-04-13*
