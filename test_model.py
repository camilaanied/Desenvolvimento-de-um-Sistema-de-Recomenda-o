from recomendador.model import RecommenderSystem 

if __name__ == "__main__":
    print("Carregando o modelo...")
    rec = RecommenderSystem()

    user_id = 1  # depois testar outros IDs
    print(f"\nGerando recomendações para o usuário {user_id}...\n")

    recomendacoes = rec.recommend(user_id, k=5)

    if not recomendacoes:
        print("Nenhuma recomendação encontrada. o usuário pode não existir.")
    else:
        for r in recomendacoes:
            print(f"Filme: {r['movieId']}  |  Score: {r['score']:.4f}")

    print("\nTeste concluído.")
