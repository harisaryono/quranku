from transformers import MarianMTModel, MarianTokenizer

# Fungsi untuk menerjemahkan teks
def translate(text, src_lang='en', tgt_lang='id'):
    # Menentukan model yang digunakan untuk terjemahan
    model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
    
    # Memuat model dan tokenizer
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    
    # Tokenisasi input teks
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    
    # Menerjemahkan teks
    translated = model.generate(**inputs)
    
    # Dekode hasil terjemahan
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_text

# Contoh penggunaan
src_text = "Hello, how are you?"
translated_text = translate(src_text, 'en', 'id')
print(f"Original: {src_text}")
print(f"Translated: {translated_text}")

