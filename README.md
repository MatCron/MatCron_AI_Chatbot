# AI Chatbot

## Overview
This AI chatbot is built using FastAPI and OpenAI's API. The chatbot leverages a fine-tuned model stored in a JSON file to improve responses based on specific training data. The API allows users to interact with the chatbot through HTTP requests.

## Planning Phases
The initial planning, there are a total of 3 phases which included:

### Phase 1 - Completed 
Completed the chatbot with colleced data and fine tuned it.

### Phase 2 - Completed
Completed the text-to-speech and speech-to-text implementation.

### Phase 3 - Future Feature
Unfinished Chatbot AI automation which help user in completing the request automatically based on the user provided information. Hence, this is not completed as due to time constraint. It will be added to the future features.

## Features
- Uses OpenAI's API key for communication with the GPT model.
- FastAPI framework for handling API requests.
- Fine-tuned model configuration stored in a JSON file.
- Supports text-based interaction via API endpoints.

## Security
- Implemented the Authentication based on the JWT token to check and validate the user exist in the database

## Requirements
- Python 3.8+
- fastapi
- uvicorn[standard]
- aiomysql
- pymysql
- python-dotenv
- sqlalchemy
- pydantic
- openai
- PyJWT

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup
1. Get an OpenAI API key from [OpenAI's website](https://openai.com/).
2. Create a `.env` file in the project root and add your API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```
3. Ensure your fine-tuned model JSON file is in place and correctly formatted.

## Running the API
Start the FastAPI server using Uvicorn:
```bash
uvicorn main:app --reload
```

The API will be available at: `ws://127.0.0.1:8000` or `ws://localhost:8000`

## API Endpoints
### Send Message to Chatbot
**Notes:** This is a websocket connection to receive a realtime information. 
**Endpoint:** `ws/chat`
**Request Body:**
```json
{
  "message": "Hello, chatbot!"
}
```

**Response Example:**
```json
{
  "response": "Hello! How can I assist you today?"
}
```

## Deployment
To deploy on a cloud server:
- Use Docker or set up a FastAPI environment on a VPS.
- Configure environment variables securely.
- Set up a process manager (e.g., `systemd` or `gunicorn`) to keep the server running.
- Remember to set up a dotenv file for replacing the database and OpenAI api key inside.

## Frontend implementation for phase 1 and 2
Sample screen after the implemetation

![Flutter Implemetation](https://i.ibb.co/B2CN1w06/image.png)


## License
This project is licensed under the MIT License.

