from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from recomendador.model import RecommenderSystem

app = FastAPI(
    title="API - Sistema de Recomendação",
    description="Recomenda filmes usando filtragem colaborativa (MovieLens 100k).",
    version="1.0.0"
)

# Carrega o modelo uma única vez
recommender = RecommenderSystem()

# Schemas da API


class RatingIn(BaseModel):
    user_id: int
    movie_id: int
    rating: float


class UserIn(BaseModel):
    user_id: int


class ItemIn(BaseModel):
    movie_id: int
    title: str | None = None  # o  título é apenas informativo aqui



# Rotas

@app.get("/")
def root():
    return {"message": "API do Sistema de Recomendação está ativa!"}


@app.get("/recommend/{user_id}")
def get_recommendation(user_id: int, k: int = 10):
    recs = recommender.recommend(user_id, k)

    if not recs:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado na matriz de recomendações ou sem recomendações disponíveis."
        )

    return {"user_id": user_id, "recommendations": recs}


@app.post("/rating")
def add_rating(rating: RatingIn):
    if rating.rating < 0 or rating.rating > 5:
        raise HTTPException(
            status_code=400,
            detail="A avaliação deve estar entre 0 e 5."
        )

    recommender.add_rating(rating.user_id, rating.movie_id, rating.rating)

    return {"message": "Avaliação adicionada e modelo atualizado."}


@app.post("/user")
def add_user(user: UserIn):
    """
    Registra um novo usuário no sistema.
    As recomendações só aparecem depois que ele começar a avaliar filmes.
    """
    created = recommender.add_user(user.user_id)

    if not created:
        raise HTTPException(
            status_code=400,
            detail="Usuário já existe no sistema."
        )

    return {"message": "Usuário criado com sucesso.", "user_id": user.user_id}


@app.post("/item")
def add_item(item: ItemIn):
    """
    Registra um novo item (filme). O título é opcional e aqui serve
    apenas como metadado; o modelo em si usa apenas o movie_id.
    """
    created = recommender.add_item(item.movie_id)

    if not created:
        raise HTTPException(
            status_code=400,
            detail="Item (filme) já existe no sistema."
        )

    return {
        "message": "Item criado com sucesso.",
        "movie_id": item.movie_id,
        "title": item.title
    }