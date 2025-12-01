import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity


class RecommenderSystem:
    """
    Sistema simples de recomendação baseado em Filtragem Colaborativa
    por similaridade entre usuários (User-based Collaborative Filtering).
    """

    def __init__(self, ratings_path: str | None = None):
        # Descobre o caminho padrão do arquivo ratings.csv (dentro de recomendador/data)
        if ratings_path is None:
            base_dir = Path(__file__).resolve().parent
            ratings_path = base_dir / "data" / "ratings.csv"

        # Carrega avaliações
        self.ratings = pd.read_csv(ratings_path)

        # Converte tipos
        self.ratings["userId"] = self.ratings["userId"].astype(int)
        self.ratings["movieId"] = self.ratings["movieId"].astype(int)
        self.ratings["rating"] = self.ratings["rating"].astype(float)

        # Conjunto de usuários e itens conhecidos
        self.users = set(self.ratings["userId"].unique())
        self.items = set(self.ratings["movieId"].unique())

        # Inicializa estruturas
        self.user_item_matrix = None
        self.similarity_matrix = None

        # Treina o modelo ao iniciar
        self.train()

    def train(self) -> None:
        """
        Monta a matriz usuário x item e calcula a matriz de similaridade entre usuários.
        """
        # Cria matriz de usuários (linhas) x filmes (colunas)
        self.user_item_matrix = self.ratings.pivot_table(
            index="userId",
            columns="movieId",
            values="rating"
        ).fillna(0)

        # Similaridade de cosseno entre vetores de usuários
        sim = cosine_similarity(self.user_item_matrix)

        # Guarda em DataFrame para facilitar consultas
        self.similarity_matrix = pd.DataFrame(
            sim,
            index=self.user_item_matrix.index,
            columns=self.user_item_matrix.index
        )

    def recommend(self, user_id: int, k: int = 10):
        """
        Gera recomendações para um usuário específico.
        Retorna uma lista de dicionários: {"movieId": int, "score": float}.
        """

        # Usuário não existe na matriz (nunca avaliou nada)
        if user_id not in self.user_item_matrix.index:
            return []

        # Similaridade do usuário alvo com todos os outros
        user_similarities = self.similarity_matrix.loc[user_id]

        # Pega os 10 usuários mais parecidos (ignorando o próprio usuário)
        similar_users = user_similarities.sort_values(ascending=False).iloc[1:11]

        # Avaliações desses usuários
        similar_ratings = self.user_item_matrix.loc[similar_users.index]

        # Score ponderado: soma(similaridade * rating) / soma(similaridade)
        weighted_ratings = np.dot(similar_users.values, similar_ratings)
        sim_sum = np.sum(similar_users.values)

        if sim_sum == 0:
            return []

        scores = weighted_ratings / sim_sum

        # Zera itens que o usuário já avaliou
        user_rated = self.user_item_matrix.loc[user_id]
        scores[user_rated > 0] = 0

        # Cria série com índices = movieId e valores = score
        movie_scores = pd.Series(scores, index=self.user_item_matrix.columns)

        # Seleciona top-k itens
        top_movies = movie_scores.sort_values(ascending=False).head(k)

        # Retorna em formato amigável para API
        recommendations = [
            {"movieId": int(mid), "score": float(score)}
            for mid, score in top_movies.items()
        ]

        return recommendations

    def add_rating(self, user_id: int, movie_id: int, rating: float) -> None:
        """
        Adiciona uma nova avaliação (para atualizar preferências do usuário)
        e re-treina o modelo.
        """
        new_row = {
            "userId": int(user_id),
            "movieId": int(movie_id),
            "rating": float(rating),
            "timestamp": 0, 
        }

        self.ratings = pd.concat(
            [self.ratings, pd.DataFrame([new_row])],
            ignore_index=True
        )

        # Atualiza conjuntos de usuários e itens
        self.users.add(int(user_id))
        self.items.add(int(movie_id))

        # Recalcula matriz e similaridade
        self.train()

    def add_user(self, user_id: int) -> bool:
        """
        Registra um novo usuário no sistema.
        Apenas mantém controle lógico; as recomendações só surgem
        após o usuário começar a avaliar itens.
        Retorna True se criou, False se já existia.
        """
        user_id = int(user_id)
        if user_id in self.users:
            return False

        self.users.add(user_id)
        return True

    def add_item(self, movie_id: int) -> bool:
        """
        Registra um novo item (filme) no sistema.
        Retorna True se criou, False se já existia.
        """
        movie_id = int(movie_id)
        if movie_id in self.items:
            return False

        self.items.add(movie_id)
        # O item passa a ser avaliado quando aparecer em add_rating.
        return True