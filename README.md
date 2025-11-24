## 🐳 Cómo ejecutar con Docker

1. Descargar Docker

Se puede descargar desde su sitio web: https://www.docker.com/

2. Build de la imagen

Si fue descargado Docker en Windows, accedemos a Docker Desktop, abrimos una terminal, nos movemos a la carpeta del proyecto y ejecutamos:

```bashrc
docker build -t simulacion-tdc .
```

3. Ejecutar el contenedor
```bashrc
docker run -p 3000:3000 simulacion-tdc
```

Luego abrir en el navegador: http://localhost:3000

