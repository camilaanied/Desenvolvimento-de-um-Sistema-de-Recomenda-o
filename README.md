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



Modelo de Recomendação Utilizado e Decisões de Design:

Este projeto implementa um Sistema de Recomendação baseado em Filtragem Colaborativa, utilizando especificamente o método User-Based Collaborative Filtering (UBCF).
A escolha desse modelo se deve à sua interpretabilidade, simplicidade matemática e excelente desempenho em conjuntos de dados pequenos e médios, como o MovieLens 100k.

   O modelo segue as etapas clássicas de filtragem colaborativa baseada em usuários, conforme detalhado abaixo:
- Construção da Matriz Usuário × Item: A partir dos dados presentes em ratings.csv, é construída uma matriz onde:
Linhas representam usuários, colunas representam filmes, células contêm notas (1 a 5)
Essa matriz é naturalmente esparsa, o que influencia as decisões de design adotadas.

- Cálculo da Similaridade entre Usuários:
foi utilizada a métrica:
Similaridade do Cosseno (Cosine Similarity)

Razões para essa escolha:
Funciona muito bem em dados esparsos
Mede ângulo entre vetores, ignorando magnitude
É amplamente utilizada em sistemas colaborativos
É extremamente eficiente e interpretável

- Identificação dos Usuários Mais Similares (Top-k Neighbors)

Para cada usuário, selecionam-se os k vizinhos mais parecidos, onde k = 5.
Esses vizinhos influenciam diretamente a predição de filmes não avaliados.
Justificativa para k=5:
- Reduz ruído
- Mantém diversidade de padrões
- É ideal para datasets médios como MovieLens 100k

- Predição das Notas para Filmes Não Avaliados
O sistema prevê as notas de filmes que o usuário ainda não assistiu usando uma média ponderada, onde o peso é a similaridade dos vizinhos.

Fórmula utilizada: Nota prevista = Σ(similaridade × nota) / Σ(similaridade)

Essa decisão garante:
- Menor impacto de usuários pouco similares
- Recomendação mais confiável
- Explicabilidade das predições

- Geração da Lista de Recomendações:
Após prever todas as notas faltantes:
Removem-se filmes que o usuário já avaliou
Ordenam-se as predições em ordem decrescente
Retornam-se os Top N filmes recomendados (padrão: N = 5)
Exemplo real do sistema:
{
  "user_id": 1,
  "recommendations": [
    {"movieId": 318, "score": 4.0890},
    {"movieId": 295, "score": 3.9901}
  ]
}

    Decisões de Design Tomadas:
- Escolha de User-Based vs Item-Based
Optou-se pelo User-Based porque:

É mais adequado como projeto didático
Facilita explicar por que um filme foi recomendado
Lida melhor com perfis comportamentais variáveis
Funciona muito bem em datasets como MovieLens 100k

- Similaridade do Cosseno como Métrica Principal
Alternativas (Pearson, Euclidiana) foram consideradas, porém:
Pearson exige correlação forte entre usuários
Distância Euclidiana sofre com esparsidade
Cosine é a mais estável e escalável para o caso

- Re-Treino Dinâmico após Novas Avaliações
A API foi projetada para:
Atualizar a matriz usuário × item
Recalcular similaridades
Regenerar recomendações automaticamente
Isso garante que o sistema esteja sempre atualizado.

- Uso de FastAPI para Servir o Modelo
Essa decisão foi tomada porque:
Produz documentação automática via Swagger
É extremamente rápida (ASGI)
Facilita implementação de endpoints REST
É padrão moderno em APIs de Machine Learning

- Containerização com Docker
O Dockerfile garante:
Reprodutibilidade
Ambiente controlado
Fácil implantação em qualquer servidor


- Validação com Testes Unitários
Foram desenvolvidos testes para:
Funcionamento do cálculo de similaridade
Predição de recomendações
Operações da API
A utilização de Pytest agrega:
Robustez
Reprodutibilidade



Conclusão:

Este projeto demonstra:

- Processamento de dados reais (MovieLens 100k)
- Criação de um modelo de recomendação
- Desenvolvimento de API profissional
- Testes unitários
- Containerização com Docker
- Documentação

