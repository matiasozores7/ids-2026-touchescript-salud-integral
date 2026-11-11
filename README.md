# Centro Médico Salud Integral — Sistema de Turnos Médicos con QR

## Proyecto Integrador — Introducción al Desarrollo de Software (2026)

- **Cátedra:** Lanzillotta — 2.º Cuatrimestre 2026
- **Temática:** Opción 2 — Sistema de gestión de turnos médicos con check-in por código QR
- **Grupo:** Touchescript

---

## Descripción del Proyecto

Plataforma web para el **Centro Médico Salud Integral**, orientada a digitalizar y optimizar la administración de citas médicas, eliminar solapamientos de agendas y reducir el ausentismo en la sala de espera.

El sistema contempla:

- **Frontend (Portal de Pacientes):** Registro e inicio de sesión, catálogo de especialidades y médicos, reserva de turnos online y emisión de comprobantes con código QR.
- **Backoffice (Recepción / Administración):** ABM de médicos, especialidades, consultorios y coberturas; configuración de agendas de atención; panel de sala de espera del día y escaneo y validación de códigos QR para el check-in.
- **Backend (API RESTful):** Arquitectura modular desarrollada con Flask, conectada a MySQL mediante consultas SQL explícitas.

---

## Documentación

Para obtener más información sobre los requerimientos, especificaciones y condiciones del proyecto, visitá la [Wiki del repositorio](https://github.com/matiasozores7/ids-2026-touchescript-salud-integral/wiki)).

## Tecnologías y Arquitectura

De acuerdo con las restricciones técnicas de la asignatura:

- **Backend:** Python 3.x + Flask (API RESTful con respuestas JSON y prefijo `/api`).
- **Frontend / Backoffice:** Flask Server-Side Rendering (SSR), con consumo de la API REST mediante la librería `requests` de Python. No se utilizan ORMs ni peticiones asíncronas desde el navegador, como `fetch` o `axios`.
- **Base de Datos:** MySQL con consultas SQL explícitas y parametrizadas (PyMySQL).
- **Seguridad y Autenticación:** Manejo de sesiones y cifrado de contraseñas mediante `werkzeug.security`.
- **Validación y Check-in:** Generación y validación de tokens QR para confirmar la asistencia de los pacientes a la sala de espera.

---

## Estructura del Repositorio

```text
ids-2026-touchescript-salud-integral/
├── backend/
│   ├── scripts/              # Scripts auxiliares
│   └── src/
│       ├── database/         # Conexión y acceso a MySQL
│       ├── errors/           # Manejo de excepciones
│       ├── repositories/     # Consultas SQL y acceso a datos
│       ├── routes/           # Endpoints de la API REST
│       ├── services/         # Lógica de negocio
│       ├── utils/            # Utilidades generales
│       └── validators/       # Validaciones de entrada
│
├── database/                 # Scripts de base de datos
│
└── frontend/
    ├── app/
    │   ├── clients/          # Comunicación con el backend
    │   ├── constants/        # Constantes de la aplicación
    │   ├── errors/           # Manejo de errores
    │   ├── routes/
    │   │   ├── backoffice/   # Rutas administrativas
    │   │   └── patient/      # Rutas del portal de pacientes
    │   ├── services/         # Servicios de la aplicación
    │   └── utils/            # Utilidades generales
    │
    ├── static/
    │   ├── css/              # Hojas de estilo
    │   ├── img/              # Recursos gráficos
    │   └── js/               # Scripts JavaScript
    │
    └── templates/
        ├── backoffice/       # Plantillas administrativas
        ├── coberturas/       # Gestión de coberturas
        ├── dashboards/       # Paneles de control
        ├── pacientes/        # Portal de pacientes y reservas
        └── recepcion/        # Gestión de recepción y check-in
```

---

## Instalación e Inicialización

### 1. Clonar el repositorio

```bash
git clone https://github.com/matiasozores7/ids-2026-touchescript-salud-integral.git
cd ids-2026-touchescript-salud-integral
```

### 2. Ejecutar el script de inicialización

Otorgar permisos de ejecución al script `init.sh` para crear el entorno virtual e instalar las dependencias necesarias:

```bash
chmod +x init.sh
./init.sh
```

### 3. Configurar las variables de entorno

Copiar la plantilla `.env.example` y completar los datos correspondientes a la conexión con la base de datos MySQL local y las claves secretas necesarias:

```bash
cp .env.example .env
```

### 4. Inicializar la base de datos

Cargar el esquema de la base de datos en el servidor MySQL:

```bash
mysql -u tu_usuario -p tu_base_de_datos < database/schema.sql
```

---

## Ejecución del Sistema

Para ejecutar la solución completa, es necesario levantar ambos servidores en terminales independientes.

### Terminal 1: Servidor Backend (API REST)

```bash
cd backend
python app.py
```

> El servidor estará disponible en `http://localhost:5000/api`.

### Terminal 2: Servidor Frontend (Web App / Backoffice)

```bash
cd frontend
python run.py
```

> El portal web estará disponible en `http://localhost:5001`.
