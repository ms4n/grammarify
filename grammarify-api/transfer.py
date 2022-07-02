import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, T5Tokenizer, T5ForConditionalGeneration
from adequacy import Adequacy
import warnings

warnings.filterwarnings("ignore")

torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'

adequacy = Adequacy()

ctf_tokenizer = AutoTokenizer.from_pretrained("sanjay-m1/informal-to-formal", cache_dir="models/")
ctf_model = AutoModelForSeq2SeqLM.from_pretrained("sanjay-m1/informal-to-formal", cache_dir="models/")
print("[Transfer] - Informal to Formal model loaded.")

grammar_tokenizer = T5Tokenizer.from_pretrained('sanjay-m1/grammar-corrector-v2', cache_dir="models/")
grammar_model = T5ForConditionalGeneration.from_pretrained('sanjay-m1/grammar-corrector-v2', cache_dir="models/")\
    .to(torch_device)
print("[Transfer] - Grammar Corrector model loaded.")

model_loaded = True