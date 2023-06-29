import openai
import os

# Cargar la variable de entorno desde el archivo .env
from dotenv import load_dotenv
load_dotenv()

# Obtener la clave de API de OpenAI de la variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

#Definición de las historias de usuario
user_stories = {
    'hu1': {'story': 'Create voyage', 'dependencies': ['hu12', 'hu3'], 'points': 3},
    'hu2': {'story': 'Handle Cargo Event', 'dependencies': ['hu12'], 'points': 3},
    'hu3': {'story': 'Add Carrier Movement', 'dependencies': ['hu12'], 'points': 5},
    'hu4': {'story': 'Create Location', 'dependencies': [], 'points': 2},
    'hu5': {'story': 'View Tracking', 'dependencies': [], 'points': 3},
    'hu6': {'story': 'Create Cargo', 'dependencies': ['hu7', 'hu9', 'hu11'], 'points': 7},
    'hu7': {'story': 'Route Cargo', 'dependencies': ['hu8'], 'points': 5},
    'hu8': {'story': 'Create Leg', 'dependencies': ['hu12'], 'points': 2},
    'hu9': {'story': 'Book Cargo', 'dependencies': ['hu12'], 'points': 5},
    'hu10': {'story': 'Change Cargo Destination', 'dependencies': ['hu12'], 'points': 1},
    'hu11': {'story': 'Create Delivery', 'dependencies': ['hu6', 'hu13', 'hu14'], 'points': 7},
    'hu12': {'story': 'Get Locations', 'dependencies': [], 'points': 2},
    'hu13': {'story': 'Get Carrier Status', 'dependencies': ['hu5'], 'points': 3},
    'hu14': {'story': 'Get Routes Status', 'dependencies': ['hu5'], 'points': 3}
}

#Generación de prompt 
prompt = """
Given the following user stories with their dependencies and estimated points:
{user_stories}

Design a microservice architecture that satisfies the requirements of the system .

Design a microservice distribution that can handle these user stories efficiently, ensuring scalability, reliability, and maintainability. Describe the key microservices, their responsibilities, and the interactions between them. 
Must consider the dependencies of the stories and their estimated points.

Design a microservice architecture that must use semantic similiraty to define the microservices.

Must minimize the number of microservices by taking into account dependencies between user stories.

Must minimize the number of calls between user stories that are in different microservices.

Must reduce the number of microservice to the minimun posible.

The number of user stories in a microserver increases it complexity, you must reduce the complexity of microservices
by keeping the minimun number of microservices
Instructions:
1. Provide a detailed description of the microservice architecture, including the following:

a. Identify the key microservices and their responsibilities.
b. Explain the technique of design and why use it
c. Explain the number of microservices
d. Explain how the dependencies of the user stories affect the final microservice architecture

2. For each microservice identified, list the user stories it handles with their estimated points. For example:
    - Microservice: Voyage Service
      - User Stories:
        - Create voyage hu1
        - Handle Cargo Event hu2
        - Add Carrier Movement hu3

Feel free to include diagrams or any other supporting material to illustrate your design.
""".format(
    user_stories="\n".join([
        f"{key}: {val['story']} (Dependencies: {', '.join(val['dependencies'])}, Points: {val['points']})" for key, val in user_stories.items()
    ])
)

#Funcion que conecta con la api de OPENAI
def get_completion(conversation, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=conversation,
        temperature=0.7,
    )
    return response.choices[0].message["content"]

def chat_with_model():
    initial_prompt = prompt
    conversation = [
        {"role": "user", "content": initial_prompt}
    ]
    
    while True:
        user_input = input("User: ")
        conversation.append({"role": "user", "content": user_input})
        
        completion = get_completion(conversation)
        print("Model:", completion)
        
        conversation.append({"role": "assistant", "content": completion})
        
        if "bye" in user_input.lower():
            break

chat_with_model()

