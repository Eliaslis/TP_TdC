## 🐳 Cómo ejecutar con Docker
1. Build de la imagen

Desde la carpeta del proyecto:

```bashrc
docker build -t simulacion-tdc .
```

2. Ejecutar el contenedor
```bashrc
docker run -p 8080:8080 simulador-cicd
```

Luego abrir en el navegador: http://localhost:8080

## ▶️ Cómo ejecutar de forma local

1. Instalar Node.js

Descargar desde https://nodejs.org

2. Instalar dependencias (si corresponde)

Este proyecto no requiere dependencias externas, pero se recomienda instalar http-server para servir el HTML fácilmente:

```bashrc
npm install -g http-server
```

3. Levantar el servidor local

Ejecutar:

```bashrc
http-server .
```

Y abrir http://localhost:8080


