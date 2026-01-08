# SSTI Scanner & Exploiter (Smarty, Mako, Jinja2)

Herramienta en Python para la **detección automática de vulnerabilidades Server-Side Template Injection (SSTI)** en aplicaciones web y su **explotación interactiva**, con soporte inicial para los motores de plantillas:

- Smarty
- Mako
- Jinja2

El script analiza formularios HTML, identifica parámetros inyectables y prueba payloads específicos para detectar y, en caso afirmativo, ejecutar comandos del sistema remoto.

## Características

- Descubrimiento automático de formularios e inputs HTML.
- Detección de SSTI mediante evaluación aritmética.
- Identificación específica del motor de plantillas:
  - Smarty
  - Mako
  - Jinja2
- Explotación interactiva en caso de SSTI Mako.
- Ejecución de comandos del sistema (`id`, `ls`, etc.) a través de payloads ofuscados.
- Compatible con sistemas Linux y Windows (para limpieza de pantalla).

## Requisitos

- Python 3.8+
- Conectividad HTTP hacia el objetivo
- Aplicación objetivo vulnerable a SSTI

## Instalación

Clona el repositorio y crea un entorno virtual (opcional pero recomendado):

```bash
git clone https://github.com/Rod-hex/STTI-Python.git
cd STTI-Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 SSTI.py
```

## Uso

URL: http://victima.local/search

