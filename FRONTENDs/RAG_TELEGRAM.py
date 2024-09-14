import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import telebot

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Inicializa el bot de Telegram con el token desde las variables de entorno
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

# Configuración de ChatOpenAI
chat = ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0.7
)

# Mensajes de contexto inicial para ChatOpenAI
messages = [
        SystemMessage(content="You are a motivational assistant with a warm and informal tone. Your primary focus is to provide motivation and encouragement. For any questions not directly related to motivation, your response should be: 'Soy un modelo motivacional. Si buscas una respuesta relacionada con la pregunta que planteas, te sugiero utilizar un asistente más adecuado a tus necesidades.' Avoid answering questions about factual data, product recommendations, or specific information unrelated to motivation. Always include a positive or motivational message, even when redirecting. If you don´t find anything in source_knowledge you have to answer 'Lo siento no dispongo de información al respecto'."),
    HumanMessage(content="Hi AI, how are you today?"),
    AIMessage(content="I'm great, thank you! I'm here to motivate and inspire you. How can I help you feel more empowered today?"),
    HumanMessage(content="I'd like to know how to be happy.")
]

# Configuración del cliente Qdrant con las variables de entorno
qdrant = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_KEY"))

# Configuración del modelo de embeddings
embeddings_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

# Función para construir el prompt y manejar la consulta
def custom_prompt(query: str, collection_name: str):
    # Generación del embedding de la consulta
    query_embedding = embeddings_model.encode([query])[0].tolist()

    # Búsqueda en Qdrant
    results = qdrant.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=3
    )

    # Extracción del texto de la carga útil
    source_knowledge = "\n".join([result.payload.get("text", "No text available") for result in results])

    # Construcción del prompt aumentado
    augment_prompt = f"""Using the contexts below, answer the query:

    Contexts:
    {source_knowledge}

    Query: {query}"""

    return augment_prompt

# Función principal para manejar las consultas (sin ponderación, solo con y sin stopwords)
def handle_query(query: str, use_stopwords: bool):
    collection_name = "OnlyContent_withStopwords" if use_stopwords else "OnlyContent_withoutStopwords"
    prompt = HumanMessage(content=custom_prompt(query, collection_name))
    messages.append(prompt)
    res = chat.invoke(messages)
    return res.content

# Manejo del comando '/start' en Telegram
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy Teddy, tu bot motivacional.")

# Manejo de mensajes de texto en Telegram
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    query = message.text
    response = handle_query(query, use_stopwords=True)  # Usamos la BBDD con stopwords
    bot.reply_to(message, response)

# Mantiene el bot en funcionamiento
bot.infinity_polling()
