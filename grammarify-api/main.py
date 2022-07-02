from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from corrector import formal_transfer, grammar_corrector


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
