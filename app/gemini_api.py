import google.generativeai as genai
from config import GOOGLE_API_KEY
from PIL import Image

genai.configure(api_key=GOOGLE_API_KEY)

def identify_plant(image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = "Identify this plant and provide the following information in JSON format: name,scientificName,description,family,nativeRegion,growthHabit,flowerColor,leafType. Do not use any markdown formatting in your response. Just return the raw JSON."
    
    response = model.generate_content([prompt, image])
    return response.text