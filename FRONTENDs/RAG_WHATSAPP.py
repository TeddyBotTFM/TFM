import os
from twilio.rest import Client
from langchain_openai import ChatOpenAI
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from flask import Flask, request, jsonify
import threading
import time

#Variables de entorno
os.environ['OPENAI_API_KEY'] = 'credenciales.txt'
os.environ['QDRANT_URL'] = 'credenciales.txt'
os.environ['QDRANT_KEY'] = 'credenciales.txt'

# Configura tus credenciales de Twilio
account_sid = 'credenciales.txt'
auth_token = 'credenciales.txt'
twilio_number= 'credenciales.txt'

#Iniciamos el cliente de Twilio
client = Client(account_sid, auth_token)

# Configuración de ChatOpenAI
chat = ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0.7
)

# Función principal para manejar las consultas
def handle_query(query: str, use_stopwords: bool):
    collection_name = "OnlyContent_withStopwords" if use_stopwords else "OnlyContent_withoutStopwords"
    prompt = HumanMessage(content=custom_prompt(query, collection_name))
    messages = [
        SystemMessage(content="You are a motivational assistant with a warm and informal tone. Your primary focus is to provide motivation and encouragement. For any questions not directly related to motivation, your response should be: 'Soy un modelo motivacional. Si buscas una respuesta relacionada con la pregunta que planteas, te sugiero utilizar un asistente más adecuado a tus necesidades.' Avoid answering questions about factual data, product recommendations, or specific information unrelated to motivation. Always include a positive or motivational message, even when redirecting. If you don´t find anything in source_knowledge you have to answer 'Lo siento no dispongo de información al respecto'."),
        HumanMessage(content="Hi AI, how are you today?"),
        AIMessage(content="I'm great, thank you! I'm here to motivate and inspire you. How can I help you feel more empowered today?"),
        HumanMessage(content="I'd like to know how to be happy."),
        prompt
    ]
    res = chat.invoke(messages)
    return res.content

# Configuración del cliente Qdrant
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
    source_knowledge = "\n".join([result.payload.get("text", "No text available") for result in results])
    augment_prompt = f"""Using the contexts below, answer the query:
    Contexts:
    {source_knowledge}
    Query: {query}"""
    return augment_prompt

# Funciones para enviar y recibir mensajes
def send_whatsapp_message(to, body):

    try:
        # Enviar el mensaje con Twilio
        message = client.messages.create(
            body=body,
            from_=f'whatsapp:{twilio_number}',
            to=f'{to}'
        )
        return message.sid
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")
        return None

# Recibir y manejar mensajes de WhatsApp
def receive_whatsapp_message(request):
    incoming_msg = request.form.get('Body')
    from_number = request.form.get('From')

    # Manejo del comando 'start' o cualquier otro mensaje
    if not incoming_msg or not from_number:
        return jsonify({"status": "no message or sender found"}), 400

    if incoming_msg.lower() == 'start':
        welcome_message = "¡Hola! Soy Teddy, tu bot motivacional. ¿En qué puedo ayudarte hoy?"
        send_whatsapp_message(from_number, welcome_message)
        return jsonify({"status": "message processed"}), 200

    else:
        # Manejo de cualquier mensaje de texto
        response = handle_query(incoming_msg, use_stopwords=True)  # Usando la BBDD con stopwords
        send_whatsapp_message(from_number, response)
        return jsonify({"status": "message not processed"}), 200

app = Flask(__name__)


# Ruta para recibir mensajes desde WhatsApp (Twilio Webhook)

@app.route('/webhook', methods=['POST'])
def webhook():
    return receive_whatsapp_message(request)

def run_flask():
  app.run(host="0.0.0.0", port=4000)

def run_localtunnel():
  time.sleep(5)
  !lt --port 4000

  # Iniciar Flask en un hilo separado
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

localtunnel_thread = threading.Thread(target=run_localtunnel)
localtunnel_thread.start()

!lt --port 4000

