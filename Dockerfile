# Imagem base do Python
FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia as dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto para dentro do container
COPY . .

# Expõe a porta usada pela API
EXPOSE 8000

# Comando para iniciar a API dentro do container
CMD ["uvicorn", "recomendador.main:app", "--host", "0.0.0.0", "--port", "8000"]