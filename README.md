# Plantilla Flask + SQLite + Tailwind CSS

Proyecto de demostración para gestionar clientes con Flask, SQLite, HTML,
JavaScript y Tailwind CSS. Sirve como plantilla base para futuros proyectos:
incluye una arquitectura por capas, validaciones en el servidor, mensajes
flash, datos de ejemplo y CSS compilado localmente.

La aplicación no usa el CDN de Tailwind ni necesita Node.js para ejecutarse.
El archivo `app/static/css/output.css` está versionado y listo para usarse.

## Características

- Patrón de fábrica `create_app()` y Blueprint para clientes.
- Base de datos SQLite creada automáticamente.
- Tres clientes de ejemplo insertados solo si la tabla está vacía.
- Listado, creación y edición de clientes.
- Validación de nombre, correo y teléfono en el servidor.
- Mensajes de éxito y error que pueden cerrarse desde JavaScript.
- Diseño adaptable con Tailwind CSS compilado localmente.

## Estructura

```text
.
├── app/
│   ├── __init__.py              # Fábrica de la aplicación y ruta raíz
│   ├── config.py                # Configuración por variables de entorno
│   ├── database.py              # Flask-SQLAlchemy y creación de tablas
│   ├── models/
│   │   ├── __init__.py
│   │   └── cliente.py           # Modelo Cliente
│   ├── routes/
│   │   ├── __init__.py
│   │   └── clientes.py          # Rutas HTTP del Blueprint de clientes
│   ├── services/
│   │   └── cliente_service.py   # Consultas, validaciones y lógica
│   ├── static/
│   │   ├── css/
│   │   │   ├── input.css        # Entrada de Tailwind
│   │   │   └── output.css       # CSS compilado y versionado
│   │   ├── js/
│   │   │   └── main.js          # Cierre de notificaciones
│   │   └── img/
│   │       └── README.md
│   └── templates/
│       ├── base.html            # Estructura, navegación y mensajes
│       └── clientes/
│           ├── index.html       # Listado de clientes
│           └── form.html        # Formulario para crear y editar
├── .env.example
├── .gitignore
├── app.py                       # Punto de entrada
├── README.md
└── requirements.txt
```

La carpeta `instance/` y el archivo SQLite se crean al iniciar la aplicación.
Están ignorados por Git porque son datos locales.

## Requisitos

- Python 3.10 o superior.
- Node.js y npm solo para volver a compilar Tailwind. No son necesarios para
  ejecutar la demo.

## Instalación en Windows

Abre PowerShell en la raíz del proyecto y ejecuta:

```powershell
# 1. Crear y activar el entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Instalar dependencias
python -m pip install --upgrade pip
pip install -r requirements.txt

# 3. Preparar las variables de entorno
Copy-Item .env.example .env
```

Si PowerShell bloquea la activación del entorno virtual, puedes usar el Python
del entorno directamente sin cambiar la política del sistema:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

El archivo `.env` es opcional para la demo: `config.py` usa SQLite y una clave
de desarrollo si no existe. Puedes ajustar `SECRET_KEY` o `DATABASE_URL`
copiando `.env.example`.

## Ejecutar la aplicación

Con el entorno virtual activo:

```powershell
python app.py
```

Abre <http://127.0.0.1:5000>. La ruta `/` redirige a `/clientes/` y muestra el
listado con tres clientes de ejemplo.

Para reiniciar los datos de la demo, detén el servidor, elimina
`instance/clientes.db` y vuelve a iniciar la aplicación. Las tablas se crean y
los ejemplos se cargan de nuevo solo si la tabla está vacía.

## Compilar Tailwind CSS sin dejar Node en el proyecto

El proyecto no incluye `package.json`, `package-lock.json` ni `node_modules`.
Tailwind se instala en una carpeta temporal fuera del repositorio y el CSS
compilado se escribe directamente en `app/static/css/output.css`.

### Compilación minificada (equivalente a `build`)

Desde la raíz del proyecto en PowerShell:

```powershell
$raiz = (Get-Location).Path -replace '\\', '/'
$tailwind = Join-Path $env:TEMP "tailwind-demo-flask"
New-Item -ItemType Directory -Force -Path $tailwind | Out-Null

Push-Location $tailwind
npm init -y
npm install tailwindcss@3.4.17
npx tailwindcss -i "$raiz/app/static/css/input.css" -o "$raiz/app/static/css/output.css" --content "$raiz/app/templates/**/*.html,$raiz/app/static/js/**/*.js" --minify
Pop-Location

Remove-Item -Recurse -Force $tailwind
```

### Observar cambios (equivalente a `dev`)

Mantén el entorno temporal y usa `--watch`. La primera vez crea la carpeta e
instala Tailwind:

```powershell
$raiz = (Get-Location).Path -replace '\\', '/'
$tailwind = Join-Path $env:TEMP "tailwind-demo-flask"
New-Item -ItemType Directory -Force -Path $tailwind | Out-Null

Push-Location $tailwind
npm init -y
npm install tailwindcss@3.4.17
npx tailwindcss -i "$raiz/app/static/css/input.css" -o "$raiz/app/static/css/output.css" --content "$raiz/app/templates/**/*.html,$raiz/app/static/js/**/*.js" --watch
```

Cuando termines, presiona `Ctrl+C`, ejecuta `Pop-Location` y elimina la carpeta
temporal:

```powershell
Pop-Location
Remove-Item -Recurse -Force $tailwind
```

Tailwind detecta clases en `app/templates/**/*.html` y
`app/static/js/**/*.js`. Si agregas clases nuevas a otros archivos, incluye sus
rutas en el argumento `--content`.

## Flujo de uso

1. `GET /clientes/` muestra todos los clientes ordenados por nombre.
2. `GET /clientes/nuevo` muestra el formulario de creación.
3. `POST /clientes/nuevo` valida y guarda un cliente.
4. `GET /clientes/<id>/editar` carga el formulario con los datos actuales.
5. `POST /clientes/<id>/editar` valida y actualiza el cliente.

Las validaciones y el acceso a datos están en
`app/services/cliente_service.py`; las rutas solo orquestan peticiones y
respuestas. La tabla se compone de `nombre`, `correo` y `telefono`. El correo es
único y se normaliza a minúsculas.

## Notas de la plantilla

- El CSS se enlaza únicamente mediante
  `{{ url_for('static', filename='css/output.css') }}`.
- `input.css` contiene las directivas de Tailwind y los componentes
  reutilizables (`btn-primary`, `btn-secondary`, `form-label`, `form-input`).
- `output.css` debe regenerarse después de modificar el diseño, las plantillas o
  las clases detectadas en JavaScript.
- No se incluyen autenticación, Docker ni funcionalidades adicionales para
  mantener la demo sencilla.
