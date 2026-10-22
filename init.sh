#!/bin/bash

echo "=== Configurando entorno ==="

if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv || python -m venv venv
fi

# Detectar si está en Windows (Scripts) o Linux/Mac (bin)
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "Error: no se encontró el activador del entorno virtual."
    exit 1
fi

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "=== Entorno configurado ==="