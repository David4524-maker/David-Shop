# David Shop

¡Bienvenido a **David Shop**! Una plataforma unificada de distribución y simulación de aplicaciones desarrollada completamente en **Python 3.14** utilizando `Tkinter` para la interfaz gráfica y `SQLite3` para la gestión local de datos.

Este proyecto simula una tienda de aplicaciones legítima con un catálogo de más de 1000 productos automatizados, divididos en juegos de Steam, Epic Games, aplicaciones nativas, utilidades, suscripciones y juegos interactivos en HTML5.

##  Características Principales
*   **Diseño Moderno:** Soporte nativo para temas Claro (`Light`) y Oscuro (`Dark`).
*   **Logo en Canvas:** El logo de David Shop está renderizado vectorialmente mediante código utilizando el Canvas de Tkinter.
*   **Juegos HTML5 Jugables:** Los juegos de la categoría HTML se descargan localmente y son jugables de verdad (incluye *Snake, Pong, Tetris, Flappy Bird, 2048, Buscaminas*, entre otros) abriéndose directamente en tu navegador.
*   **Sistema de Carrito y Cupones:** Gestión completa de compras simuladas con cálculo de impuestos (16%) y soporte para cupones de descuento activos (ej. `DAVID10`, `LEGIT20`).
*   **Panel de Administración:** Panel oculto para gestionar usuarios, productos, exportar reportes de pedidos a formato CSV y realizar copias de seguridad de la base de datos.
*   **Soporte Internacional (i18n):** Traducido dinámicamente a tres idiomas: Español (ES), Inglés (EN) y Portugués (PT).

##  Requisitos Mínimos
*   **Python 3.14** o superior.
*   **Git** (para clonar este repositorio).
*   No requiere instalar librerías externas de terceros (`pip`), ya que utiliza exclusivamente los módulos nativos del ecosistema estándar de Python (`tkinter`, `sqlite3`, `threading`, etc.).

##  Instalación y Uso Rápido

Sigue estos pasos en tu terminal o línea de comandos para arrancar la tienda en tu computadora:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com
   cd DavidShop
   ```

2. **Iniciar la aplicación:**
   ```bash
   python main.py
   ```

##  Credenciales de Acceso
Al iniciar por primera vez, puedes registrar una cuenta nueva o ingresar directamente al panel de administración con las credenciales por defecto:
*   **Usuario:** `admin`
*   **Contraseña:** `admin123`

##  Estructura de Descargas
Por defecto, todo el software o juego HTML adquirido a través de la tienda se descargará de manera real en tu carpeta de usuario del sistema, dentro del directorio: `~/David_Shop_Downloads`.

---
*David Shop · Hecho con fines educativos y de portafolio · 100% legítimo 😉*
