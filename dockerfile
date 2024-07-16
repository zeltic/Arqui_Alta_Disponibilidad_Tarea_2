FROM python:3.9

# Instalar cron y vim (vim es opcional, útil para editar archivos si es necesario)
RUN apt-get update && apt-get install -y cron vim

COPY . /app

RUN pip install -r /app/requirements.txt

ARG POSTGRES_DB
ENV POSTGRES_DB=${POSTGRES_DB}

ARG POSTGRES_USER
ENV POSTGRES_USER=${POSTGRES_USER}

ARG POSTGRES_PASSWORD
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}

ARG POSTGRES_HOST
ENV POSTGRES_HOST=${POSTGRES_HOST}

ARG POSTGRES_PORT
ENV POSTGRES_PORT=${POSTGRES_PORT}

# Dar permiso de ejecución al script
RUN chmod +x /app/my_script.py

# Añadir el cronjob al crontab del root
RUN (crontab -l 2>/dev/null; echo "*/1 * * * * /usr/local/bin/python /app/my_script.py >> /var/log/cron.log 2>&1") | crontab -

# Crear el archivo log para capturar la salida de cron
RUN touch /var/log/cron.log

# Ejecutar cron en primer plano
CMD cron -f
