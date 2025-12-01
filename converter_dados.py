import pandas as pd
from pathlib import Path

# Descobre a pasta do projeto que é onde está este arquivo
BASE_DIR = Path(__file__).resolve().parent

# Procura os arquivos u.data, u.item e u.user em qualquer subpasta
try:
    u_data_path = next(BASE_DIR.rglob("u.data"))
    u_item_path = next(BASE_DIR.rglob("u.item"))
    u_user_path = next(BASE_DIR.rglob("u.user"))
except StopIteration:
    raise FileNotFoundError("Não encontrei u.data / u.item / u.user em nenhuma subpasta. Confere se o ml-100k foi extraído dentro do projeto.")

print(f"Usando dataset em: {u_data_path.parent}")

# Garante que a pasta recomendador/data existe
data_dir = BASE_DIR / "recomendador" / "data"
data_dir.mkdir(parents=True, exist_ok=True)

# Converter u.data p/ ratings.csv
cols = ["userId", "movieId", "rating", "timestamp"]
df = pd.read_csv(u_data_path, sep="\t", names=cols)
df.to_csv(data_dir / "ratings.csv", index=False)
print(f"Criado: {data_dir / 'ratings.csv'}")

# Converter u.item p/ movies.csv
cols = ["movieId", "title", "release_date", "video_release", "url"] + [f"g{i}" for i in range(19)]
df = pd.read_csv(u_item_path, sep="|", names=cols, encoding="latin-1")
df[["movieId", "title"]].to_csv(data_dir / "movies.csv", index=False)
print(f"Criado: {data_dir / 'movies.csv'}")

# Converter u.user p/ users.csv
cols = ["userId", "age", "gender", "occupation", "zip"]
df = pd.read_csv(u_user_path, sep="|", names=cols)
df.to_csv(data_dir / "users.csv", index=False)
print(f"Criado: {data_dir / 'users.csv'}")
