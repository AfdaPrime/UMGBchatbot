import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

# Must Change back to GPU
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = torch.device('cpu')

with open('UMGBintents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data_UMGB.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"
print("Let's chat! (type 'quit' to exit)")


def chat(sentence):

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                response = random.choice(intent['responses'])
                # print(f"{bot_name}: {response}")
    else:
        response = "I'm sorry, but I can't answer that question at the moment due to my limited knowledge on certain topics. However, you can ask your buddies by texting them or reach out to the ISC officers by emailing them for further assistance. I apologize for any inconvenience."
        # print(f"{bot_name}: {response}.")
    return response
