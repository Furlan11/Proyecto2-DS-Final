# Proyecto 2 DS

## ¿Cómo levantar el contenedor?

### Obtener la imagen

```bash
docker pull diggspapu/data-science-environment
```

### Construir el contenedor

```bash
docker build -t data-science .
```

### Levantar el contenedor

```bash
docker run --gpus all -p 8811:8811 -v "$(pwd):/app" --name data-science-container -d data-science
```

### Levantar el contenedor cuando ya se creo el contenedor

```bash
docker start -i data-science-container
```

## ¿Cómo levantar la Aplicación?

```bash
docker compose up --build
```
