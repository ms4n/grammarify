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
grammar_model = T5ForConditionalGeneration.from_pretrained('sanjay-m1/grammar-corrector-v2', cache_dir="models/") \
    .to(torch_device)
print("[Transfer] - Grammar Corrector model loaded.")

model_loaded = True


def transfer(input_sentence, style, quality_filter=0.95):
    if style == 0:
        output_sentence = _casual_to_formal(input_sentence, torch_device, quality_filter)
        return output_sentence
    # if style == 1:
    #     output_sentence = _correct_grammar(input_sentence)
    #     return output_sentence

    else:
        print("Models aren't loaded for this style, please use the right style during init.")


def _casual_to_formal(input_sentence, device, quality_filter, max_candidates=5):
    ctf_prefix = ""
    src_sentence = input_sentence
    input_sentence = ctf_prefix + input_sentence
    input_ids = ctf_tokenizer.encode(input_sentence, return_tensors='pt')
    input_ids = input_ids.to(device)

    predictions = ctf_model.generate(
        input_ids,
        do_sample=True,
        max_length=32,
        top_k=50,
        top_p=0.95,
        early_stopping=True,
        num_return_sequences=max_candidates)

    gen_sentences = set()
    for prediction in predictions:
        gen_sentences.add(ctf_tokenizer.decode(prediction, skip_special_tokens=True).strip())

    adequacy_scored_phrases = adequacy.score(src_sentence, list(gen_sentences), quality_filter, device)
    ranked_sentences = sorted(adequacy_scored_phrases.items(), key=lambda x: x[1], reverse=True)
    if len(ranked_sentences) > 0:
        return ranked_sentences[0][0]
    else:
        return None
