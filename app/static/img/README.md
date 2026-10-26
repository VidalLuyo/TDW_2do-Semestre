# Imágenes

Guarda aquí los recursos gráficos locales del proyecto (logotipos, íconos o
ilustraciones). Esta carpeta se mantiene en el repositorio aunque esté vacía
para conservar la estructura de la plantilla.

Puedes referenciar una imagen desde las plantillas Jinja así:

```html
<img src="{{ url_for('static', filename='img/mi-imagen.png') }}" alt="Descripción">
```

No se incluyen imágenes de ejemplo para evitar archivos binarios innecesarios.
