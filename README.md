# SSTI Scanner & Exploiter (Smarty · Mako · Jinja2)

Herramienta en Python para la **detección automática de vulnerabilidades Server-Side Template Injection (SSTI)** en aplicaciones web y su **explotación interactiva limitada**, basada en el análisis de formularios HTML y la inyección de payloads específicos por motor de plantillas.

El proyecto está concebido como una **prueba de concepto (PoC)** orientada a entornos controlados (laboratorios y CTFs).

## Aviso importante sobre el alcance del proyecto

Esta herramienta **no funciona en todas las aplicaciones web** ni pretende hacerlo.

El script ha sido diseñado como una **prueba de concepto (PoC)** para escenarios muy concretos y controlados, donde se cumplen determinadas condiciones técnicas.

### Aplicaciones compatibles (escenarios típicos)

El script está orientado a aplicaciones que:

- Utilizan **formularios HTML clásicos** (`<form>` / `<input>`).
- Envían parámetros mediante el método **GET**.
- Renderizan directamente los parámetros dentro de un **motor de plantillas del lado servidor**.
- Emplean motores compatibles con los payloads probados (Smarty, Mako, Jinja2).
- No aplican un filtrado o escape estricto del input antes de la renderización.

Este tipo de escenarios es habitual en:
- Laboratorios de práctica (CTFs, Hack The Box, VulnHub).
- Aplicaciones legacy.
- Desarrollos educativos o mal configurados.

### Aplicaciones no compatibles

La herramienta **no funcionará** (o lo hará de forma muy limitada) en:

- Single Page Applications (React, Angular, Vue).
- Formularios enviados mediante JavaScript (`fetch`, `XHR`, `AJAX`).
- APIs REST que procesan parámetros en **JSON**.
- Inyección a través de headers, cookies u otros vectores no soportados.
- Motores de plantillas distintos a los probados.
- Aplicaciones con WAF o sanitización básica de expresiones SSTI.
- Contextos donde el input no llega directamente al template.

Estas limitaciones son **deliberadas** y forman parte del enfoque del proyecto.

## Motores de plantillas soportados

- **Smarty**  
  Detección mediante evaluación aritmética y comentarios.  
  La explotación no está automatizada; se proporciona un payload de referencia.

- **Mako**  
  Detección y **explotación interactiva funcional**, con ejecución de comandos del sistema mediante `os.popen`.

- **Jinja2**  
  Detección mediante evaluación aritmética.  
  La explotación no está automatizada; se proporciona un payload de referencia.

## Características

- Descubrimiento automático de formularios HTML (`<form>`).
- Enumeración de parámetros a partir de inputs `<input name=...>`.
- Envío de payloads SSTI mediante peticiones HTTP GET.
- Detección de SSTI mediante evaluación aritmética controlada.
- Identificación del motor de plantillas:
  - Smarty
  - Mako
  - Jinja2
- Explotación interactiva en caso de SSTI **Mako**:
  - Verificación de ejecución (`id`)
  - Shell interactiva basada en ejecución de comandos
- Extracción básica de output desde la respuesta HTML.
- Limpieza de salida inicial (`id && comando`) para mostrar únicamente el resultado relevante.
- Compatible con sistemas Linux y Windows (limpieza de pantalla).

## Requisitos

- Python 3.8+
- Conectividad HTTP hacia el objetivo
- Aplicación vulnerable a SSTI reflejada en HTML
- Entorno de pruebas autorizado

Dependencias principales:
- `requests`
- `beautifulsoup4`

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

## Funcionamiento del script

El script realiza las siguientes acciones:

- Analiza los formularios HTML presentes en la página objetivo.
- Prueba cada parámetro identificado con payloads específicos de SSTI.
- Identifica el motor de plantillas vulnerable, en caso de existir.
- En el caso de **Mako**, permite continuar con una fase de explotación interactiva.

## Funcionamiento de la explotación (Mako)

- Se verifica la ejecución remota mediante el comando `id`.
- A partir de ese punto, el usuario puede introducir comandos arbitrarios.
- Internamente se utiliza `id && <comando>` como marcador de ejecución.
- El output se post‑procesa para eliminar el primer `id` y mostrar únicamente el resultado del comando solicitado.

## Limitaciones conocidas

Este proyecto **no es una herramienta universal** y presenta limitaciones deliberadas:

- Solo analiza formularios HTML estáticos.
- No soporta:
  - Formularios generados dinámicamente mediante JavaScript.
  - Parámetros en formato JSON.
  - Inyección a través de headers o cookies.
  - Métodos HTTP distintos de `GET`.
- La extracción del output es heurística y dependiente de la estructura HTML de la respuesta.
- No existe una separación estricta entre la fase de detección y la de explotación.
- No se implementan técnicas de evasión de WAF.
- No se gestiona la salida de error (`stderr`) ni errores complejos.

## Advertencias y alcance del proyecto

Este proyecto ha sido desarrollado con fines **exclusivamente educativos y de investigación**, en el contexto de laboratorios controlados (CTFs, Hack The Box y entornos de práctica).

- No está diseñado para uso en entornos de producción.
- La funcionalidad de explotación incluida es experimental y limitada.
- El código no está optimizado ni refactorizado en esta fase.
- Pueden existir falsos positivos y falsos negativos.

El autor no se responsabiliza del uso indebido de esta herramienta fuera de entornos controlados o sin autorización explícita.


