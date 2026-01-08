# SSTI Scanner & Exploiter (Smarty, Mako, Jinja2)

Herramienta en Python para la **detección automática de vulnerabilidades Server-Side Template Injection (SSTI)** en aplicaciones web y su **explotación interactiva**, con soporte inicial para los motores de plantillas:

- Smarty (Apartadp de explotación en desarrollo)
- Mako
- Jinja2 (Apartado de explotación en desarrollo)

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
```

## Uso

```shell-session
python3 SSTI.py
URL: http://<IP:PORT>
```

## Advertencias y alcance del proyecto

Este proyecto ha sido desarrollado con fines **exclusivamente educativos y de investigación**, en el contexto de laboratorios controlados (CTFs y entornos de práctica como Hack The Box).

Aspectos a tener en cuenta:

- La herramienta se concibe como una **prueba de concepto (PoC)** para la detección de vulnerabilidades de Server-Side Template Injection (SSTI).  
  No pretende ser una solución genérica ni lista para uso en entornos de producción.

- Aunque el objetivo principal es la **detección**, el código incluye lógica experimental de explotación con fines demostrativos.  
  Cualquier uso de estas funcionalidades debe realizarse **únicamente sobre sistemas propios o con autorización explícita**.

- El código **no está comentado ni optimizado** deliberadamente en esta fase, priorizando la funcionalidad y la validación del concepto.  
  Se prevé una futura refactorización orientada a mejorar legibilidad, modularidad y mantenibilidad.

- La detección se basa en **heurísticas y payloads específicos**, por lo que pueden existir falsos positivos o falsos negativos dependiendo del motor de plantillas y del contexto de ejecución.

- La herramienta no implementa actualmente:
  - Gestión avanzada de errores
  - Separación estricta entre detección y explotación
  - Soporte completo para todos los métodos HTTP
  - Normalización de salidas según tipo de contenido

El autor no se responsabiliza del uso indebido de esta herramienta fuera de entornos controlados o sin el consentimiento adecuado.
