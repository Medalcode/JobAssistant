# Lista de Issues para JobAssistant Project 🚀

Esta lista contiene las tareas pendientes, mejoras sugeridas y bugs potenciales para poblar el GitHub Project.

## 🔴 Alta Prioridad (In Progress / Next Up)

### 1. Integración de API LLM (OpenAI/DeepSeek)
- **Descripción:** Reemplazar la lógica heurística actual de `CareerStrategist` por llamadas reales a una API de IA.
- **Detalles:** 
  - Configurar `OPENAI_API_KEY`.
  - Crear prompts system para resumen de perfil y análisis de gaps.
- **Labels:** `enhancement`, `AI`, `backend`

### 2. Sistema de Autenticación de Usuarios
- **Descripción:** Permitir a los usuarios registrarse y guardar sus datos permanentemente.
- **Detalles:**
  - Implementar Login/Registro (JWT o OAuth con Google).
  - Migrar `localStorage` a base de datos PostgreSQL por usuario.
  - Crear Dashboard de usuario.
- **Labels:** `feature`, `security`, `database`

### 3. Rotación de Proxies para Scraper
- **Descripción:** Evitar bloqueos en Computrabajo mediante el uso de proxies.
- **Detalles:**
  - Integrar soporte para proxies rotativos (ej. ScraperAPI, BrightData) en `scrapers/computrabajo.py`.
  - Manejar reintentos automáticos tras error 403.
- **Labels:** `bug`, `scraping`, `infrastructure`

---

## 🟡 Media Prioridad (To Do)

### 4. Generador de Cartas de Presentación (Cover Letter Agent)
- **Descripción:** Nuevo agente que escriba cartas personalizadas para cada oferta.
- **Detalles:**
  - Crear `agents/cover_letter_writer.py`.
  - Input: CV del usuario + Descripción del trabajo.
  - Output: Texto o PDF de la carta.
- **Labels:** `feature`, `AI`, `agents`

### 5. Interfaz de Feedback de Agentes
- **Descripción:** Mostrar al usuario qué están "pensando" los agentes en el frontend.
- **Detalles:**
  - Crear un componente de UI (Toast o Log) que muestre: "Buscando en Computrabajo...", "Analizando compatibilidad ATS...", "Optimizando CV...".
  - Conectar backend (WebSockets o Polling) con frontend.
- **Labels:** `frontend`, `UX`

### 6. Soporte Multi-País en Scraper
- **Descripción:** Extender el scraper para soportar otros dominios de Computrabajo (MX, CO, PE, AR).
- **Detalles:**
  - Parametrizar la URL base en `run(location="Mexico")`.
  - Detectar automáticamente el dominio correcto.
- **Labels:** `scraping`, `enhancement`

---

## 🟢 Baja Prioridad / Futuro (Backlog)

### 7. Análisis de Salarios de Mercado
- **Descripción:** Agente que estime el rango salarial para el perfil del usuario.
- **Detalles:**
  - Scrapear salarios de ofertas similares.
  - Generar gráfica comparativa.
- **Labels:** `data-science`, `feature`

### 8. Exportación a LinkedIn/JSON Resume
- **Descripción:** Permitir exportar los datos en formatos estándar.
- **Detalles:**
  - Formato JSON Resume (estándar open source).
  - Texto plano optimizado para copiar-pegar en LinkedIn.
- **Labels:** `feature`, `export`

### 9. Tests E2E con Playwright
- **Descripción:** Automatizar pruebas de flujo completo (Frontend + Backend).
- **Detalles:**
  - Simular usuario llenando formulario -> Generando PDF -> Verificando descarga.
- **Labels:** `testing`, `QA`
