from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from corrector import formal_transfer, grammar_corrector

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"grammar_correction": "/grammar-correct",
            "formal_translation": "/formal_translate"}


@app.post("/grammar-correct")
async def correct_sentence(incorrect_sentence: str):
    response = grammar_corrector(incorrect_sentence)
    return response


@app.post("/formal_translate")
async def formal_translation(casual_sentence: str):
    response = formal_transfer(casual_sentence)
    return response
