from recomendador.model import RecommenderSystem


def test_recommend_returns_list():
    rec = RecommenderSystem()
    recomendacoes = rec.recommend(user_id=1, k=5)

    # Deve retornar uma lista
    assert isinstance(recomendacoes, list)

    # No máximo k itens
    assert len(recomendacoes) <= 5

    # Se houver recomendações, cada uma deve ter movieId e score
    if recomendacoes:
        primeira = recomendacoes[0]
        assert "movieId" in primeira
        assert "score" in primeira
