import praw
import csv
from googletrans import Translator

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
total_results = 50  # Puedes cambiar este valor según tus necesidades

# Lista para almacenar todos los resultados
all_results = []

# Realiza múltiples solicitudes para obtener más resultados
for submission in subreddit.search(search_query, limit=total_results):
    all_results.append(submission)

# Nombre del archivo CSV
csv_file = "resultados.csv"

# Abre el archivo CSV en modo escritura y escribe los resultados
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Define el orden de los campos en el encabezado del CSV
    header = ["ID", "Autor", "URL", "Puntuación", "Cantidad de Comentarios", "Creado", "Texto Original", "Texto Traducido"]

    # Escribe la fila de encabezados en el archivo CSV
    writer.writerow(header)

    # Configura el traductor
    translator = Translator()

    # Itera a través de todos los resultados y escribe cada conjunto de datos en una fila del archivo CSV
    for submission in all_results:
        # Traduce el título al español
        titulo_es = translator.translate(submission.title, src='auto', dest='es').text
        # Escribe los datos en el CSV en el orden especificado
        row = [submission.id, submission.author, submission.url, submission.score, submission.num_comments, submission.created_utc, submission.title, titulo_es]
        writer.writerow(row)

print(f'Se han exportado exitosamente {len(all_results)} resultados a {csv_file}.')
