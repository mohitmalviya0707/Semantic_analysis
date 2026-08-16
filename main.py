from tensorflow.keras.preprocessing.sequence import pad_sequences
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from keras.models import load_model
from keras.layers import Embedding, Dense

import numpy as np
import pickle
import re


# ============================================================
# 1. CONSTANTS
# ============================================================

# A. Model Path
model_path = "Artifacts/BiGRU_Model_fixed.keras"

# B. Tokenizer Path
tokenizer_path = "Artifacts/tokenizer.pkl"

# C. Maximum Sequence Length
max_sequence_length = 50

# D. Emotion Labels
emotion_labels = [
    "sadness",
    "joy",
    "love",
    "anger",
    "fear",
    "surprise"
]

# E. Emotion Emojis
EMOTION_EMOJIS = {
    "sadness": "😢",
    "joy": "😄",
    "love": "❤️",
    "anger": "😠",
    "fear": "😨",
    "surprise": "😲",
}


# ============================================================
# 2. TEXT PREPROCESSING
# ============================================================

def preprocess_text(text: str) -> str:
    """
    Cleans raw text so that it matches
    the preprocessing used during training.
    """

    # Convert to lowercase
    text = text.lower()

    # Remove apostrophes
    text = re.sub(r"'", "", text)

    # Remove special characters and punctuation
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ============================================================
# 3. REQUEST / RESPONSE SCHEMAS
# ============================================================

class TextInput(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The sentence to analyze",
        json_schema_extra={
            "example": "I feel so happy and excited"
        }
    )


class PredictionResponse(BaseModel):
    text: str
    predicted_emotion: str
    confidence: float
    all_probabilites: dict[str, float]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


# ============================================================
# 4. MODEL STORAGE
# ============================================================

dl_model = {}


# ============================================================
# 5. MODEL LOADING
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Loading the model and tokenizer...")

    try:

        # ----------------------------------------------------
        # Load BiGRU model
        # ----------------------------------------------------

        dl_model["BiGRU"] = load_model(
            model_path,
            compile=False
        )

        print("BiGRU model loaded successfully.")

        # ----------------------------------------------------
        # Load tokenizer
        # ----------------------------------------------------

        with open(tokenizer_path, "rb") as file:
            dl_model["Tokenizer"] = pickle.load(file)

        print("Tokenizer loaded successfully.")
        print("Model and tokenizer are loaded successfully.")

    except Exception as e:

        print("ERROR while loading model/tokenizer:")
        print(e)

        # Clear partially loaded objects
        dl_model.clear()

        raise

    yield

    # --------------------------------------------------------
    # Clear model from memory when server shuts down
    # --------------------------------------------------------

    dl_model.clear()

    print("Model and tokenizer removed from memory.")


# ============================================================
# 6. FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Emotion Classification API",
    description="BiGRU based Emotion Classification API",
    version="1.0.0",
    lifespan=lifespan
)


# ============================================================
# 7. CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 8. STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# ============================================================
# 9. HOME PAGE
# ============================================================

@app.get("/", include_in_schema=False)
def server_ui():

    return FileResponse(
        "static/index.html"
    )


# ============================================================
# 10. HEALTH CHECK
# ============================================================

@app.get(
    "/health",
    response_model=HealthResponse
)
def health_check():

    return HealthResponse(
        status="Server is running",
        model_loaded=bool(dl_model)
    )


# ============================================================
# 11. EMOTION PREDICTION
# ============================================================

@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict_emotion(text_input: TextInput):

    """
    Prediction pipeline:

    1. Clean input text
    2. Convert words into numbers using tokenizer
    3. Pad sequence
    4. Run BiGRU prediction
    5. Find highest probability emotion
    6. Return complete prediction
    """

    # --------------------------------------------------------
    # Get model and tokenizer
    # --------------------------------------------------------

    BiGRU_model = dl_model.get("BiGRU")
    tokenizer_model = dl_model.get("Tokenizer")

    if BiGRU_model is None or tokenizer_model is None:

        raise HTTPException(
            status_code=503,
            detail="Model is not loaded yet. Please try again later."
        )

    # --------------------------------------------------------
    # 1. Preprocess text
    # --------------------------------------------------------

    cleaned_text = preprocess_text(
        text_input.text
    )

    # --------------------------------------------------------
    # 2. Tokenize text
    # --------------------------------------------------------

    tokenized_text = tokenizer_model.texts_to_sequences(
        [cleaned_text]
    )

    # --------------------------------------------------------
    # 3. Pad sequence
    # --------------------------------------------------------

    padded_sequence = pad_sequences(
        tokenized_text,
        maxlen=max_sequence_length,
        padding="post",
        truncating="post"
    )

    # --------------------------------------------------------
    # 4. Model prediction
    # --------------------------------------------------------

    probabilities = BiGRU_model.predict(
        padded_sequence,
        verbose=0
    )[0]

    # --------------------------------------------------------
    # 5. Find predicted emotion
    # --------------------------------------------------------

    top_emotion_index = int(
        np.argmax(probabilities)
    )

    predicted_emotion = emotion_labels[
        top_emotion_index
    ]

    confidence = float(
        probabilities[top_emotion_index]
    )

    # --------------------------------------------------------
    # 6. Create probability dictionary
    # --------------------------------------------------------

    all_probabilites = {
        label: float(probability)
        for probability, label
        in zip(probabilities, emotion_labels)
    }

    # --------------------------------------------------------
    # 7. Return response
    # --------------------------------------------------------

    return PredictionResponse(
        text=text_input.text,
        predicted_emotion=predicted_emotion,
        confidence=confidence,
        all_probabilites=all_probabilites
    )