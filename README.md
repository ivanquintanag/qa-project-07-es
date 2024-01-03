# Ejecución de Pruebas de Python con Selenium en PyCharm

Este repositorio contiene un ejemplo básico de cómo ejecutar pruebas automatizadas de Python utilizando Selenium en el editor PyCharm.

# Requisitos Previos

Asegúrate de tener instalado Python en tu sistema. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).

Instala PyCharm si aún no lo tienes. Puedes descargarlo desde [jetbrains.com/pycharm/download/](https://www.jetbrains.com/pycharm/download/).

# Configuración del Proyecto en PyCharm

*Clona el Repositorio:*

   _git clone https://github.com/tu_usuario/tu_proyecto.git_

1. Abre el Proyecto en PyCharm:

Abre PyCharm.
Selecciona "Open" y navega hasta el directorio del proyecto clonado.
Abre el proyecto.

2. Instala Dependencias:

Abre la terminal en PyCharm.
Ejecuta el siguiente comando para instalar las dependencias necesarias:

_pip install -r requirements.txt_

# Configuración de Selenium
Descarga el Controlador de Chrome:

Descarga el controlador de Chrome (ChromeDriver) desde ChromeDriver Downloads.
Guarda el archivo en una ubicación accesible.
Actualiza la Ruta del Controlador en el Código:

Abre tu script de prueba Python en PyCharm.
Encuentra la línea que inicializa el controlador de Chrome y actualiza la ruta al archivo ChromeDriver descargado.

_path_to_chromedriver = '/ruta/del/chromedriver'_

# Ejecución de las Pruebas

1. Ejecuta el Script de Prueba:

Abre la terminal en PyCharm.
Ejecuta el script de prueba con el siguiente comando:

_python nombre_del_script.py_

2. Observa la Ejecución:

PyCharm abrirá una ventana de Chrome y ejecutará las pruebas automatizadas.
Verifica la consola de PyCharm para obtener información detallada sobre la ejecución.
