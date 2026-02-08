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

## Esquema de base de datos
El esquema esta en `schema.sql` y se inicializa automaticamente en `data/cv.db` al arrancar la app.
