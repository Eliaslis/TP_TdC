## 🐳 Cómo ejecutar con Docker
1. Build de la imagen

Desde la carpeta del proyecto:

```bashrc
docker build -t simulacion-tdc .
```

2. Ejecutar el contenedor
```bashrc
docker run -p 3000:3000 simulacion-tdc
```

Luego abrir en el navegador: http://localhost:3000

