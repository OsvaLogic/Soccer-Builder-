# Soccer Builder

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

## Descripción
**Soccer Builder** es una aplicación web interactiva que te permite armar alineaciones de fútbol personalizadas. Incluye una pizarra táctica donde puedes organizar a tus jugadores arrastrándolos y soltándolos en el campo.

## Características

- **Pizarra Interactiva:** Arrastra y suelta (*Drag & Drop*) a los jugadores libremente en la cancha.
- **Gestión de Plantillas:** Crea, edita estadísticas y guarda las alineaciones de tus equipos.
- **Formaciones Tácticas:** Cambia rápidamente entre distintas formaciones base.
- **Autenticación:** Sistema de usuarios seguro, preparado para integración con Google (OAuth).
- **Diseño Limpio:** Interfaz amigable, minimalista y fácil de usar.

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/OsvaLogic/Soccer-Builder-.git
   cd Soccer-Builder-
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate
   ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   Crea un archivo `.env` en la raíz del proyecto para colocar tus credenciales (`SECRET_KEY`, `DEBUG`, bases de datos).

5. **Aplicar migraciones y ejecutar el servidor:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## Tecnologías
- **Backend:** Django 4.2+
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla ES6)
- **Base de Datos:** SQLite (Desarrollo) / PostgreSQL (Producción)