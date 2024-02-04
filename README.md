# EasyShopBot

Welcome to EasyShopBot, a cutting-edge chatbot that transforms your shopping experience! 🛍️

## Project Overview

```plaintext
📁 ChatBotShop
|
├── 📂 action
|   └── action.py         # Refactored file handling user actions (e.g., viewing and searching products)
|
├── 📂 data
|   ├── nlu.yml           # Intent sample examples for model training
|   ├── rules.yml         # Rules triggering actions based on user interactions
|   └── stories.yml       # Training stories for understanding chat movements
|
├── 📂 model
|   ├── ...               # Stored model files essential for chatbot functioning
|
├── config.yml            # Configuration file specifying policy techniques, algorithms, and tuning parameters
|
├── credentials.yml       # File holding necessary credentials
|
├── domain.yml            # Main configuration file including actions, intents, entities, and slots
|
└── endpoints.yml         # Specification of chatbot webhook endpoint
```

## Getting Started

These instructions will help you set up and run the EasyShopBot project on your local machine.

### Prerequisites

Make sure you have the following installed on your machine:

- Python 3.x
- RASA NLU
- Other dependencies (install using `pip install -r requirements.txt`)

### Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:hrushikesh009/EasyShopBot.git
   ```

2. Navigate to the project directory:

   ```bash
   cd EasyShopBot
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Train the RASA model:

   ```bash
   rasa train
   ```

5. Run the RASA server:

   ```bash
   rasa run -m models --enable-api --cors "*"
   ```

### Usage

Visit the RASA API endpoint to interact with EasyShopBot:

   ```bash
   http://localhost:5005
   ```

Feel free to ask about products, search for items, and complete purchases right from the chat interface!

