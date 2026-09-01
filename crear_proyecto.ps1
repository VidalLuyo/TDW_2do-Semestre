# Nombre del proyecto
$Proyecto = "mi-proyecto"

# Crear carpetas
New-Item -ItemType Directory -Force -Path "$Proyecto/app/routes"
New-Item -ItemType Directory -Force -Path "$Proyecto/app/static/css"
New-Item -ItemType Directory -Force -Path "$Proyecto/app/static/img"
New-Item -ItemType Directory -Force -Path "$Proyecto/app/static/js"

# Crear archivos
New-Item -ItemType File -Force -Path "$Proyecto/app/templates/base.html"
New-Item -ItemType File -Force -Path "$Proyecto/app/__init__.py"
New-Item -ItemType File -Force -Path "$Proyecto/app.py"
New-Item -ItemType File -Force -Path "$Proyecto/requirements.txt"

Write-Host ""
Write-Host "Estructura creada correctamente." -ForegroundColor Green