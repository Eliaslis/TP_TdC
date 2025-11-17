# Imagen base oficial de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar los archivos de la aplicación al contenedor
COPY . /app

# Instalar dependencias necesarias
RUN pip install --no-cache-dir streamlit numpy pandas plotly

# Exponer el puerto de Streamlit
EXPOSE 8501

# Comando por defecto para ejecutar la app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]