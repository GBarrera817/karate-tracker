# 🥋 Karate Tracker

Aplicación web para el seguimiento del entrenamiento en karate: registro de sesiones, técnicas practicadas, control de asistencia y progresión de cinturones. Cada practicante puede llevar la bitácora de su avance y cada sensei puede gestionar a sus alumnos y sus promociones de grado.

Proyecto full-stack construido con una arquitectura desacoplada: una API REST en **Django + Django REST Framework** consumida por un frontend en **React**.

> **Estado:** 🚧 En desarrollo. El backend está en construcción; el frontend llegará una vez estabilizada la API.

---

## 📋 Tabla de contenidos

- [Motivación](#-motivación)
- [Stack tecnológico](#-stack-tecnológico)
- [Modelo de datos](#-modelo-de-datos)
- [Funcionalidades (MVP)](#-funcionalidades-mvp)
- [Requisitos previos](#-requisitos-previos)
- [Instalación y ejecución](#-instalación-y-ejecución)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Roadmap](#-roadmap)
- [Autora](#-autora)

---

## 💡 Motivación

Nació de una necesidad propia: llevar registro real del entrenamiento de karate (sesiones, técnicas y progresión de cinturón) en lugar de anotarlo en papel. Es también un proyecto de aprendizaje para dominar el desarrollo web moderno con una arquitectura desacoplada front/back, más allá de las herramientas low-code.

El dominio no es trivial a propósito: exige relaciones entre entidades, reglas de negocio (¿cumple un alumno los requisitos para el siguiente cinturón?) y control de acceso por roles. Justo lo que hace interesante un backend.

---

## 🛠 Stack tecnológico

### Backend
- **Python** 3.12+
- **Django** 5.1+
- **Django REST Framework** — API REST
- **django-cors-headers** — comunicación con el frontend (distinto origen)
- **pipenv** — gestión de entorno y dependencias
- **SQLite** en desarrollo (migrable a PostgreSQL en producción)

### Frontend *(próximamente)*
- **React** + **Vite**
- **Tailwind CSS**

### Infraestructura *(previsto)*
- Backend: Railway / Render
- Frontend: Vercel

---

## 🗄 Modelo de datos

| Entidad | Descripción |
|---|---|
| **Practicante** | Extiende el usuario de Django. Incluye rol (alumno / sensei) y cinturón actual. |
| **Cinturón** | Catálogo ordenado de grados, con los requisitos para alcanzarlos (nº mínimo de sesiones, técnicas exigidas). |
| **Técnica** | Catálogo de técnicas por categoría (kihon / kata / kumite) y cinturón mínimo. |
| **Sesión** | Registro de entrenamiento de un practicante (fecha, duración, dojo, notas) y las técnicas practicadas. |
| **Asistencia** | Marca de presencia/ausencia asociada a una sesión, registrada por el sensei. |
| **Promoción** | Historial de ascensos de grado: quién promovió a quién, de qué cinturón a cuál y cuándo. |

Relaciones clave: claves foráneas entre las entidades, una relación muchos-a-muchos entre Sesión y Técnica, y lógica de negocio sobre la progresión de cinturones.

---

## ✨ Funcionalidades (MVP)

- [ ] Autenticación con dos roles: **alumno** y **sensei**
- [ ] El alumno registra sus sesiones y marca las técnicas practicadas
- [ ] Vista de progresión: sesiones y técnicas que faltan para el siguiente cinturón
- [ ] El sensei visualiza a sus alumnos, registra asistencia y gestiona promociones
- [ ] API REST consumida por el frontend

---

## ⚙️ Requisitos previos

- Python 3.12 o superior
- pipenv (`pip install --user pipenv`)

---

## 🚀 Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/GBarrera817/karate-tracker.git
cd karate-tracker

# 2. Instalar dependencias y crear el entorno virtual
pipenv install

# 3. Activar el entorno
pipenv shell

# 4. Aplicar migraciones
python manage.py migrate

# 5. Crear un superusuario (para acceder al admin)
python manage.py createsuperuser

# 6. Levantar el servidor de desarrollo
python manage.py runserver
```

La aplicación quedará disponible en `http://localhost:8000`
y el panel de administración en `http://localhost:8000/admin`.

> **Variables de entorno:** copia `.env.example` a `.env` y define tus valores (`SECRET_KEY`, etc.) antes de ejecutar en un entorno real. El archivo `.env` no se versiona.

---

## 📁 Estructura del proyecto

```
karate-tracker/
├── config/             # Configuración del proyecto (settings, urls, wsgi)
├── entrenamiento/      # App principal: modelos, vistas, serializers, lógica
├── manage.py
├── Pipfile             # Manifiesto de dependencias
├── Pipfile.lock
├── .gitignore
└── README.md
```

---

## 🗺 Roadmap

- [x] Esqueleto del proyecto (Django + DRF + CORS)
- [ ] Modelo de datos y migraciones
- [ ] Serializers y endpoints de la API
- [ ] Autenticación y permisos por rol
- [ ] Lógica de progresión de cinturones
- [ ] Frontend en React + Vite + Tailwind
- [ ] Despliegue

### Fuera de alcance de la v1
Subida de videos, feed social, calendario, competencias, mensajería y gráficos avanzados. Reservado para versiones posteriores.

---

## 👩‍💻 Autora

**Gabriela Barrera Ángel** — Ingeniera en Computación
La Serena, Chile

---

*Proyecto de aprendizaje y portafolio.*