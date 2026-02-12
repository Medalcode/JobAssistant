
# ⚠️ No tienes instalado GitHub CLI (gh)
# Para crear automáticamente estos issues, necesitas instalarlo o hacerlo manualmente.

# Opción A: Copia y Pega estos títulos y descripciones en tu GitHub Project.

## 🔴 Alta Prioridad
1. **[Feature] Integración de API LLM (OpenAI/DeepSeek)**
   Reemplazar la lógica de `CareerStrategist` con llamadas a API real. Configurar API Keys y prompts de sistema.

2. **[Feature] Sistema de Autenticación**
   Implementar Login/Registro para guardar perfiles. Migrar de localStorage a PostgreSQL por usuario.

3. **[Bugfix] Rotación de Proxies en Scraper**
   Integrar proxies rotativos en `computrabajo.py` para evitar bloqueos 403 y mejorar la tasa de éxito.

## 🟡 Media Prioridad
4. **[Feature] Generador de Cartas de Presentación**
   Nuevo agente `CoverLetterWriter` que redacte cartas personalizadas basadas en el CV y la oferta.

5. **[UX] Feedback Visual de Agentes**
   Mostrar en el frontend qué está pensando cada agente ("Buscando...", "Analizando...", "Generando...").

6. **[Enhancement] Soporte Multi-País**
   Parametrizar el scraper para soportar dominios de Computrabajo de otros países (MX, CO, PE, AR).

## 🟢 Baja Prioridad
7. **[Analysis] Estimador de Salarios**
   Agente que scrapea y estima rangos salariales para el perfil del usuario.

8. **[Export] Exportar a JSON Resume / LinkedIn**
   Añadir opciones de exportación en formatos estándar portables.

9. **[Testing] Tests E2E con Playwright**
   Automatizar pruebas de flujo completo (fill form -> generate PDF) para asegurar calidad.
