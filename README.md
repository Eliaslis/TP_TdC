# 📘 Simulación interactiva de sistema CI/CD 
Este proyecto modela un sistema de Integración y Entrega Continua (CI/CD) como un sistema de control de lazo cerrado.
La aplicación permite experimentar de manera interactiva cómo las ganancias $K_P$, $K_I$ y $K_D$ afectan la estabilidad, el sobreimpulso y el régimen permanente del sistema.

## 🛠️ Instalación
### Opción 1: Docker
- Construir la imagen:
```bashrc
docker build -t tp-tdc .
```
- Ejecutar el contenedor:
```bashrc
docker run -p 8501:8501 tp-tdc
```
- Acceder en el navegador:
[http://localhost:8501](http://localhost:8501)

### Opción 2: Local
- Clonar el repositorio:
```bashrc
git clone https://github.com/Eliaslis/TP_TdC.git
cd TP_TdC
```
- Instalar dependencias:
```bashrc
pip install streamlit numpy pandas plotly
```
- Ejecutar la aplicación:
```bashrc
streamlit run app.py
```
- Abrir en el navegador:
[http://localhost:8501](http://localhost:8501)




# TP_TdC
