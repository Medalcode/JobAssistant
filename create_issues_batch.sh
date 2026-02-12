#!/bin/bash

GH="./bin/gh"

echo "Creating GitHub Issues..."

# High Priority
$GH issue create --title "[Feature] Integración de API LLM (OpenAI/DeepSeek)" --body "Reemplazar la lógica de `CareerStrategist` con llamadas a API real. Configurar API Keys y prompts de sistema." --label "enhancement,AI,backend"

$GH issue create --title "[Feature] Sistema de Autenticación" --body "Implementar Login/Registro para guardar perfiles. Migrar de localStorage a PostgreSQL por usuario." --label "feature,security,database"

$GH issue create --title "[Bugfix] Rotación de Proxies en Scraper" --body "Integrar proxies rotativos en `computrabajo.py` para evitar bloqueos 403 y mejorar la tasa de éxito." --label "bug,scraping,infrastructure"

# Medium Priority
$GH issue create --title "[Feature] Generador de Cartas de Presentación" --body "Nuevo agente `CoverLetterWriter` que redacte cartas personalizadas basadas en el CV y la oferta." --label "feature,AI,agents"

$GH issue create --title "[UX] Feedback Visual de Agentes" --body "Mostrar en el frontend qué está pensando cada agente ('Buscando...', 'Analizando...', 'Generando...')." --label "frontend,UX"

$GH issue create --title "[Enhancement] Soporte Multi-País" --body "Parametrizar el scraper para soportar dominios de Computrabajo de otros países (MX, CO, PE, AR)." --label "scraping,enhancement"

# Low Priority
$GH issue create --title "[Analysis] Estimador de Salarios" --body "Agente que scrapea y estima rangos salariales para el perfil del usuario." --label "data-science,feature"

$GH issue create --title "[Export] Exportar a JSON Resume / LinkedIn" --body "Añadir opciones de exportación en formatos estándar portables." --label "feature,export"

$GH issue create --title "[Testing] Tests E2E con Playwright" --body "Automatizar pruebas de flujo completo (fill form -> generate PDF) para asegurar calidad." --label "testing,QA"

echo "All issues created!"
