# ArsForte - Finanzas Personales en Contexto Inflacionario

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-6.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**ArsForte** es una aplicación web de finanzas personales diseñada para el contexto argentino, donde mantener dinero en pesos significa perder poder adquisitivo constantemente. A diferencia de las apps de finanzas genéricas, ArsForte integra datos de inflación, dólar blue, plazo fijo UVA y Bitcoin para mostrar al usuario el **costo de oportunidad real** de sus decisiones financieras.

## Características Principales

- **Registro de Transacciones**: Ingresos y gastos con instrumentos (pesos, USD, plazo fijo UVA, Bitcoin)
- **Dashboard en Tiempo Real**: Muestra ingresos, gastos, balance y valor en USD
- **Costo de Oportunidad**: Calcula cuánto habrías ganado invirtiendo en dólar blue, UVA o Bitcoin
- **Alertas Automáticas**: Notificaciones cuando más del 50% está en pesos
- **Categorización**: Sueldo, alquiler, comida, transporte, entretenimiento, servicios, inversión, ahorro
- **Seguridad**: Rate limiting, headers SSL, logging de accesos
- **Diseño Dark Glass**: Interfaz moderna con glassmorphism

## Stack Tecnológico

- **Backend**: Django 6.0
- **Base de datos**: SQLite
- **Cache**: Redis (opcional en desarrollo, requerido en producción)
- **Frontend**: Django Templates + Bootstrap 5
- **APIs externas**: Bluelytics (dólar blue), CoinGecko (Bitcoin), BCRA (UVA)

## Instalación

### Requisitos

- Python 3.10+
- Redis (opcional, para cache en desarrollo)

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/arsforte.git
cd arsforte-project
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Editá `.env` y configurá tu `SECRET_KEY`:

```env
SECRET_KEY=TU_SECRET_KEY_AQUI
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
ENV_TYPE=dev
```

### 5. Generar una nueva SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Ejecutar migraciones

```bash
python manage.py migrate
```

### 7. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 8. Iniciar el servidor

```bash
python manage.py runserver
```

Abrí http://localhost:8000 en tu navegador.

## Configuración de Producción

Para producción, configurá el archivo `.env`:

```env
SECRET_KEY=TU_SECRET_KEY_MUY_SEGURA
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
ENV_TYPE=prod

# Redis (requerido en producción)
REDIS_URL=redis://localhost:6379/0
```

## Estructura del Proyecto

```
arsforte-project/
├── arsforte/              # Configuración Django
│   └── settings/          # Settings dividido (base, dev, prod)
├── users/                  # App de autenticación
├── transactions/           # App de transacciones
├── services/               # Servicios externos (APIs)
├── security/               # Decoradores de seguridad
├── templates/              # Templates HTML
├── static/                 # CSS, JS, imágenes
├── docs/                   # Documentación
├── manage.py
├── requirements.txt
└── .env.example
```

## APIs Externas Utilizadas

| Servicio | Fuente | Datos |
|----------|--------|-------|
| Dólar Blue | Bluelytics | Cotización blue en tiempo real |
| Bitcoin | CoinGecko | Precio BTC/ARS |
| UVA | BCRA | Valor UVA y tasas |
| Inflación | Indicadores públicos | IPC mensual |

## Desarrollo

### Ejecutar tests

```bash
python manage.py test
```

### Verificar configuración

```bash
# Desarrollo
python manage.py check

# Producción
ENV_TYPE=prod python manage.py check
```

## Seguridad

- **Rate Limiting**: Límite de requests en endpoints sensibles
- **Headers SSL**: HSTS, XSS Filter, Content Type Sniffing
- **Cookies seguras**: HTTPONLY, SAME_SITE, SESSION timeout
- **Logging de accesos**: Registro de acciones de usuario

## Licencia

MIT License - Ver archivo [LICENSE](LICENSE) para más detalles.

---

*ArsForte: Entendé el verdadero costo de tus decisiones financieras.*
