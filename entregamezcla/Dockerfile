FROM python:3-alpine3.15

# Establece el directorio de trabajo
WORKDIR /app

COPY . /app

# Instala las dependencias
RUN pip install -r requirements.txt

# Expone el puerto en el que Flask se ejecutará
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "mezcla.py"]
