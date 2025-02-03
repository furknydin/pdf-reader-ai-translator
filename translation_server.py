from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# OLLAMA sunucu adresi ve model adı
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:latest"  # Modelinizin adını buraya yazın

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get("text", "")
    
    # OLLAMA API'sine istek at
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": f"Şu metni Türkçeye çevir: {text}",  # Modelden Türkçe çeviri yapmasını istiyoruz
            "stream": False  # Stream modunu kapatıyoruz, tek bir yanıt bekliyoruz
        }
        
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()  # Hata durumunda exception fırlat
        
        # OLLAMA'dan gelen yanıtı işle
        translated_text = response.json().get("response", "Çeviri başarısız oldu.")
        
        # Çevrilen metni konsola yazdır
        print(f"Orijinal Metin: {text}")
        print(f"Çevrilen Metin: {translated_text}")
    
    except Exception as e:
        translated_text = f"Hata: {str(e)}"
        print(f"Hata oluştu: {e}")
    
    return jsonify({"translated_text": translated_text})

if __name__ == "__main__":
    app.run(port=5000)