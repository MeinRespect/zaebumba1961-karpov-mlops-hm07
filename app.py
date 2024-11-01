from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List
import joblib
import uvicorn
import os

# Определение пути к файлу модели
MODEL_PATH = os.getenv("MODEL_PATH", "pipeline.joblib")


# Загрузка модели с использованием кеширования
def load_model():
    if not hasattr(load_model, "model"):
        load_model.model = joblib.load(MODEL_PATH)
    return load_model.model


# Определение FastAPI-приложения
app = FastAPI()

# Схема для входных данных
class PasswordsRequest(BaseModel):
    passwords: List[str]

# Схема для ответа
class PredictionResponse(BaseModel):
    prediction: List[float]

# Эндпоинт /predict
@app.post("/predict", response_model=PredictionResponse)
def predict(request: PasswordsRequest, model=Depends(load_model)):
    # Получение паролей из запроса
    passwords = request.passwords

    # Предсказание модели
    predictions = model.predict(passwords)

    # Возврат ответа
    return PredictionResponse(prediction=predictions.tolist())

def main():
    uvicorn.run(app, port=8000, host='0.0.0.0')

if __name__ == '__main__':
    main()
