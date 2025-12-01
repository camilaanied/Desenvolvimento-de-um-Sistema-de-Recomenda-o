Sistema de Recomendação de Filmes

Este projeto implementa um Sistema de Recomendação baseado no dataset MovieLens 100k, utilizando filtragem colaborativa (User-Based Collaborative Filtering).

Nele inclui:
- Processamento do dataset
- Modelo de recomendação
- API completa com FastAPI
- Testes unitários com Pytest 
- Containerização com Docker
- Documentação gerada automaticamente (Swagger)

Arquitetura usada no projeto:
projeto_recomendacao/
│── Dockerfile
│── requirements.txt
│── converter_dados.py
│── test_model.py
│── README.md
│
├── recomendador/
│   ├── main.py
│   ├── model.py
│   └── data/
│       ├── movies.csv
│       ├── ratings.csv
│       └── users.csv
│
└── tests/
    ├── test_model_unit.py
    └── test_api_unit.py


Dataset: MovieLens 100k
Fonte: GroupLens Research
Site oficial: https://grouplens.org/datasets/movielens/

Processamos:
- u.data → ratings.csv
- u.item → movies.csv
- u.user → users.csv
Arquivo de conversão utilizado: converter_dados.py



Modelo de Recomendação:

O modelo utiliza:

- Filtragem colaborativa baseada em usuários
- Criação de matriz usuário × item
- Similaridade do cosseno (cosine similarity)
- Cálculo das notas previstas com média ponderada
- Retorno dos itens mais relevantes para cada usuário
Arquivo principal: recomendador/model.py

API usando FastAPI:
contem endpoints para:
- GET /: verifica se o sistema está ativo
- GET /recommend/{user_id}: retorna recomendações para o usuário
- POST /user: adiciona um novo usuário ao sistema
- POST /item: registra um novo filme/item
- POST /rating: insere uma nova avaliação e re-treina o modelo


Documentação automática (Swagger)
Ao iniciar o servidor:
-  http://127.0.0.1:8000/docs
-  http://127.0.0.1:8000/redoc


Testes Unitários:
Os testes utilizam pytest e garantem: funcionamento do modelo e funcionamento dos endpoints

Para rodar os testes: python -m pytest
Saída esperada:3 passed in X.XXs

Para rodar o projeto (LOCAL):
- Instalar dependências: python -m pip install -r requirements.txt
- Iniciar o servidor FastAPI: python -m uvicorn recomendador.main:app --reload
- Acessar no navegador:
API: http://127.0.0.1:8000
Swagger: http://127.0.0.1:8000/docs


Rodar com Docker:
O projeto possui um Dockerfile funcional.
Nele construi a imagem: docker build -t recomendador-filmes . 
Executar o container: docker run -p 8000:8000 recomendador-filmes
- A API estara disponível em: http://127.0.0.1:8000/

Exemplos de requisições:

 - GET Recomendação tendo saida: 
 {
  "user_id": 1,
  "recommendations": [
    { "movieId": 318, "score": 4.0890 },
    { "movieId": 295, "score": 3.9901 },
    ...
  ]
}

- POST Novo Usuário: 
{
  "user_id": 999
}
saida:
{
  "message": "Usuário criado com sucesso.",
  "user_id": 999
}

- POST Nova Avaliação:
{
  "user_id": 999,
  "movie_id": 9999,
  "rating": 4.5
}

Conclusão:

Este projeto demonstra:

- Processamento de dados reais (MovieLens 100k)
- Criação de um modelo de recomendação
- Desenvolvimento de API profissional
- Testes unitários
- Containerização com Docker
- Documentação

