# JobAssistant

Formulario web para capturar informacion de CV y guardarla en SQLite.

## Ejecutar
1. `python -m venv .venv`
1. `. .venv/bin/activate`
1. `pip install -r requirements.txt`
1. `python app.py`

Luego abre `http://127.0.0.1:5000`.

## Probar el endpoint API

Puedes enviar una petición POST con `curl` para probar el guardado:

```bash
curl -X POST http://127.0.0.1:5000/api/submit \
	-H "Content-Type: application/json" \
	-d '{"full_name":"Tu Nombre","email":"tu@email.com"}'
```

La base de datos SQLite se crea en `data/cv.db` automáticamente.

## Despliegue en Vercel (con Supabase)

Resumen de pasos rápidos:

- Crea un proyecto en Supabase y ejecuta el SQL en `schema.sql` (Tools → SQL Editor → Run).
- En Vercel, crea un nuevo proyecto y conecta este repositorio de GitHub.
- En la configuración del proyecto en Vercel, añade las variables de entorno:
	- `SUPABASE_URL` = `https://<tu-proyecto>.supabase.co`
	- `SUPABASE_KEY` = la `service_role` key (secreta) desde Settings → API en Supabase
- Asegúrate de que `requirements.txt` incluya `requests` (ya está incluido).
- La función serverless que recibe el formulario se encuentra en `api/submit.py`.

Cuando Vercel despliegue, el frontend estático se servirá y las llamadas fetch a `/api/submit` serán manejadas por la función serverless, que insertará en Supabase.

Notas importantes:
- Usar la `service_role` key implica responsabilidad: guárdala como secreto en Vercel y no la publiques.
- Si prefieres mantener la base de datos en SQLite local, Vercel no es adecuada (filesystem es efímero).

## Esquema de base de datos
El esquema esta en `schema.sql` y se inicializa automaticamente en `data/cv.db` al arrancar la app.
