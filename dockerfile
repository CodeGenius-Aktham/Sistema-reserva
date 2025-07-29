# Usa una imagen base de Python que sea compatible con pandas.
# Python 3.10 es una excelente opción para la estabilidad con pandas 1.x o 2.x.
# La variante "slim-buster" es más ligera.
FROM python:3.10-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias de Python.
# --no-cache-dir para no guardar el caché de pip, ahorrando espacio.
# --compile para compilar los paquetes (aunque pip lo hace por defecto).
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de tu código al directorio de trabajo
COPY . .

# Expone el puerto que tu aplicación Flask escuchará.
# Render inyectará la variable de entorno $PORT.
EXPOSE $PORT

# Comando para iniciar tu aplicación Gunicorn
# Asegúrate de que 'wsgi:app' apunte correctamente a tu archivo wsgi.py y a la variable 'app'
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "wsgi:app"]