# Job Assistant 🚀

Aplicación web completa para crear CVs profesionales con asistencia de IA, búsqueda de empleos y generación de PDFs personalizados.

## 🌟 Características

### ✨ Formulario Inteligente Multi-Paso
- **6 pasos guiados** para capturar toda tu información profesional
- **Auto-guardado local** con localStorage - tus datos persisten al refrescar
- **Botón de guardado manual** en cada paso para control total
- **Validación en tiempo real** de campos requeridos

### 🤖 Generador de Perfil Profesional con IA
- Genera **3 opciones de perfil** basadas en tu experiencia y habilidades
- Análisis automático de tu título, roles y competencias
- Selección con un clic para insertar el perfil elegido

### 📄 Generación de CV en PDF
- **3 templates profesionales**: Clásico, Moderno y Uno
- Diseños optimizados para ATS (Applicant Tracking Systems)
- Descarga instantánea en formato PDF

### 💼 Búsqueda de Empleos Integrada
- Búsqueda de ofertas laborales por query y ubicación
- Aplicación directa con tu CV generado
- Registro de aplicaciones en base de datos

### 🎨 Interfaz Moderna
- Diseño responsive y profesional
- Experiencia de usuario fluida
- Feedback visual en todas las acciones

## 🚀 Demo en Vivo

**URL de producción**: [https://job-assistant-blush.vercel.app/](https://job-assistant-blush.vercel.app/)

## 📋 Estructura del Formulario

### Paso 1: Información Personal
- Nombre completo *
- Título profesional
- Ubicación
- Teléfono
- Email *
- LinkedIn
- Portafolio
- GitHub

### Paso 2: Experiencia y Educación
**Experiencia Laboral:**
- Empresa
- Cargo
- Ubicación
- Fechas (inicio/fin)
- Funciones

**Educación:**
- Institución
- Título
- Área
- Fechas (inicio/fin)
- Descripción

### Paso 3: Habilidades, Idiomas y Certificaciones
**Habilidades:**
- Nombre
- Nivel

**Idiomas:**
- Idioma
- Nivel

**Certificaciones:**
- Nombre
- Emisor
- Fecha
- URL

### Paso 4: Proyectos, Links y Perfil Profesional
**Proyectos:**
- Nombre
- Rol
- URL
- Tecnologías
- Descripción

**Links Adicionales:**
- Etiqueta
- URL

**Perfil Profesional:**
- Generación con IA (3 opciones)
- Edición manual

### Paso 5: Búsqueda de Empleo
- Query de búsqueda
- Ubicación
- Resultados con aplicación directa

### Paso 6: Selección de Template
- Vista previa de 3 diseños
- Descarga inmediata en PDF

## 🛠️ Instalación Local

### Requisitos Previos
- Python 3.8+
- pip

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/Medalcode/JobAssistant.git
cd JobAssistant
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**
```bash
python app.py
```

5. **Abrir en el navegador**
```
http://127.0.0.1:5000
```

## 🗄️ Base de Datos

### Local
- **SQLite** en `data/cv.db` (se crea automáticamente)
- Esquema definido en `schema.sql`

### Producción (Vercel)
- **SQLite efímero** en `/tmp/cv.db` (se reinicia con cada deploy)
- **Recomendado**: PostgreSQL externo (Supabase, Neon, Vercel Postgres)

Para usar PostgreSQL, configura la variable de entorno:
```bash
DATABASE_URL=postgresql://user:password@host:port/database
```

## 🌐 Despliegue en Vercel

### Configuración Automática
1. Conecta tu repositorio de GitHub a Vercel
2. Vercel detecta automáticamente la configuración de Python
3. Deploy automático en cada push a `main`

### Variables de Entorno (Opcional)
Si usas base de datos externa:
```
DATABASE_URL=postgresql://...
```

### Archivos de Configuración
- `vercel.json`: Configuración de rewrites
- `index.py`: Punto de entrada WSGI
- `requirements.txt`: Dependencias Python

## 📁 Estructura del Proyecto

```
JobAssistant/
├── app.py                 # Aplicación Flask principal
├── index.py              # Entrypoint para Vercel
├── models.py             # Modelos SQLAlchemy
├── pdf_templates.py      # Generadores de PDF
├── scraper.py            # Scraper de ofertas laborales
├── requirements.txt      # Dependencias Python
├── vercel.json          # Configuración Vercel
├── schema.sql           # Esquema de base de datos
├── static/
│   ├── app.js           # Lógica frontend
│   └── styles.css       # Estilos CSS
├── templates/
│   └── index.html       # Template principal
└── tests/               # Tests unitarios
    ├── conftest.py
    ├── test_app.py
    ├── test_pdf.py
    └── test_scraper.py
```

## 🧪 Testing

Ejecutar todos los tests:
```bash
pytest
```

Ejecutar tests específicos:
```bash
pytest tests/test_app.py
pytest tests/test_pdf.py
pytest tests/test_scraper.py
```

## 🔌 API Endpoints

### `POST /api/submit`
Guarda la información del CV en la base de datos.

**Request Body:**
```json
{
  "full_name": "Juan Pérez",
  "email": "juan@example.com",
  "professional_title": "Desarrollador Full Stack",
  "experiences": [...],
  "educations": [...],
  "skills": [...],
  ...
}
```

**Response:**
```json
{
  "status": "success",
  "candidate_id": 123
}
```

### `POST /api/generate_summary`
Genera 3 opciones de perfil profesional con IA.

**Request Body:**
```json
{
  "professional_title": "Desarrollador Full Stack",
  "experiences": [...],
  "skills": [...]
}
```

**Response:**
```json
{
  "options": [
    "Opción 1...",
    "Opción 2...",
    "Opción 3..."
  ]
}
```

### `GET /api/download/{candidate_id}?style={template}`
Descarga el CV en PDF.

**Parámetros:**
- `candidate_id`: ID del candidato
- `style`: `classic`, `modern`, o `uno`

### `GET /api/search?q={query}&location={location}`
Busca ofertas de empleo.

**Parámetros:**
- `q`: Query de búsqueda
- `location`: Ubicación

### `POST /api/apply`
Registra una aplicación a un empleo.

**Request Body:**
```json
{
  "candidate_id": 123,
  "job": {...}
}
```

## 🎨 Templates PDF

### Classic
- Diseño simple y limpio
- Ideal para ATS
- Formato de una columna

### Modern
- Elegante con acentos de color
- Estructura a dos columnas
- Tipografía Times

### Uno
- Estilo profesional
- Cabecera oscura distintiva
- Diseño minimalista

## 🔧 Tecnologías Utilizadas

### Backend
- **Flask** - Framework web
- **SQLAlchemy** - ORM
- **FPDF** - Generación de PDFs
- **Requests** - HTTP client

### Frontend
- **HTML5** - Estructura
- **CSS3** - Estilos
- **JavaScript (Vanilla)** - Lógica

### Base de Datos
- **SQLite** (local/desarrollo)
- **PostgreSQL** (producción recomendada)

### Deployment
- **Vercel** - Hosting serverless
- **Git/GitHub** - Control de versiones

## 📝 Notas Importantes

### Auto-guardado
- Los datos se guardan automáticamente en `localStorage` cada 500ms después de escribir
- Persisten al refrescar la página
- Se limpian automáticamente al enviar el formulario exitosamente

### Base de Datos en Vercel
- SQLite en `/tmp` es **efímero** - se pierde en cada reinicio
- Para datos persistentes, usa PostgreSQL externo
- Configura `DATABASE_URL` en variables de entorno de Vercel

### Seguridad
- Validación de campos requeridos
- Uso de SQLAlchemy ORM para prevenir SQL injection
- Sanitización de inputs

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👤 Autor

**Medalcode**
- GitHub: [@Medalcode](https://github.com/Medalcode)

## 🙏 Agradecimientos

- Vercel por el hosting gratuito
- FPDF por la generación de PDFs
- Flask por el excelente framework web

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!
