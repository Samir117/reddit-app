import praw
import csv
from googletrans import Translator
from datetime import datetime

# Configura las credenciales OAuth2
client_id = "cJch1PistFynpir_8PhcpQ"
client_secret = "9Cze3ghgboo6tIHc8LQ_DVquhplTxw"
user_agent = "my-app by u/m_runthat"  # Puedes personalizar esto

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
)

# Nombre del subreddit en el que deseas buscar
subreddit_name = "python"

# Término que deseas buscar
search_query = "facebook"

# Realiza la búsqueda en el subreddit
subreddit = reddit.subreddit(subreddit_name)

# Número total de resultados que deseas obtener
total_results = 150  # Puedes cambiar este valor según tus necesidades

# Lista para almacenar todos los resultados
all_results = []

# Realiza múltiples solicitudes para obtener más resultados
for submission in subreddit.search(search_query, limit=total_results):
    all_results.append(submission)

# Nombre del archivo CSV
csv_file = "resultados.csv"

# Listas para calcular la media de Puntuación y Cantidad de Comentarios
scores = []
comment_counts = []

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Escribe el encabezado
    writer.writerow(["ID", "Autor", "URL", "Puntuación", "Cantidad de Comentarios", "Creado", "Texto Original", "Texto Traducido"])

    translator = Translator()

    for submission in all_results:
        scores.append(submission.score)
        comment_counts.append(submission.num_comments)

        titulo_es = translator.translate(submission.title, src='auto', dest='es').text

        # Reemplaza '0' por la media de Puntuación y Cantidad de Comentarios
        avg_score = sum(scores) / len(scores)
        avg_comment_count = sum(comment_counts) / len(comment_counts)

        score = avg_score if submission.score == 0 else submission.score
        comment_count = avg_comment_count if submission.num_comments == 0 else submission.num_comments

        # Escribe los datos en el archivo CSV
        writer.writerow([submission.id, submission.author, submission.url, score, comment_count, submission.created_utc, submission.title, titulo_es])

print(f'Se han exportado exitosamente {len(all_results)} resultados a {csv_file}.')
