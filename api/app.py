from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import logging
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка модели и скейлера
MODEL_PATH = 'models/best_wine_model.pkl'
SCALER_PATH = 'models/scaler.pkl'

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    logger.info("Модель и скейлер успешно загружены")
except Exception as e:
    logger.error(f"Ошибка загрузки модели: {e}")
    model = None
    scaler = None

# Список признаков модели
FEATURE_NAMES = [
    'fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar',
    'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density',
    'pH', 'sulphates', 'alcohol', 'wine_type_red'
]

@app.route('/')
def home():
    """Главная страница с описанием API"""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка состояния сервиса"""
    status = "healthy" if model is not None else "unhealthy"
    return jsonify({
        'status': status,
        'timestamp': datetime.now().isoformat(),
        'model_loaded': model is not None
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Эндпоинт для предсказания качества вина"""
    try:
        if model is None:
            return jsonify({'error': 'Модель не загружена'}), 500
        
        # Получение данных из запроса
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Нет данных в запросе'}), 400
        
        # Проверка наличия всех необходимых признаков
        missing_features = [f for f in FEATURE_NAMES if f not in data]
        if missing_features:
            return jsonify({
                'error': f'Отсутствуют признаки: {missing_features}'
            }), 400
        
        # Подготовка данных для предсказания
        features = np.array([data[f] for f in FEATURE_NAMES]).reshape(1, -1)
        
        # Масштабирование признаков
        features_scaled = scaler.transform(features)
        
        # Предсказание
        prediction = model.predict(features_scaled)[0]
        prediction_proba = model.predict_proba(features_scaled)[0]
        
        # Получение вероятностей для каждого класса
        classes = model.classes_
        probabilities = {str(cls): float(prob) for cls, prob in zip(classes, prediction_proba)}
        
        result = {
            'prediction': int(prediction),
            'confidence': float(max(prediction_proba)),
            'probabilities': probabilities,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Предсказание выполнено: {prediction}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Ошибка при предсказании: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/batch', methods=['POST'])
def predict_batch():
    """Эндпоинт для пакетного предсказания"""
    try:
        if model is None:
            return jsonify({'error': 'Модель не загружена'}), 500
        
        data = request.get_json()
        
        if not data or 'samples' not in data:
            return jsonify({'error': 'Нет данных для пакетного предсказания'}), 400
        
        samples = data['samples']
        if not isinstance(samples, list):
            return jsonify({'error': 'samples должен быть списком'}), 400
        
        results = []
        
        for i, sample in enumerate(samples):
            try:
                # Проверка наличия всех необходимых признаков
                missing_features = [f for f in FEATURE_NAMES if f not in sample]
                if missing_features:
                    results.append({
                        'index': i,
                        'error': f'Отсутствуют признаки: {missing_features}'
                    })
                    continue
                
                # Подготовка данных
                features = np.array([sample[f] for f in FEATURE_NAMES]).reshape(1, -1)
                features_scaled = scaler.transform(features)
                
                # Предсказание
                prediction = model.predict(features_scaled)[0]
                prediction_proba = model.predict_proba(features_scaled)[0]
                
                results.append({
                    'index': i,
                    'prediction': int(prediction),
                    'confidence': float(max(prediction_proba))
                })
                
            except Exception as e:
                results.append({
                    'index': i,
                    'error': str(e)
                })
        
        return jsonify({
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Ошибка при пакетном предсказании: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/features', methods=['GET'])
def get_features():
    """Получение списка признаков модели"""
    return jsonify({
        'features': FEATURE_NAMES,
        'feature_descriptions': {
            'fixed_acidity': 'Фиксированная кислотность (g/L)',
            'volatile_acidity': 'Летучая кислотность (g/L)',
            'citric_acid': 'Лимонная кислота (g/L)',
            'residual_sugar': 'Остаточный сахар (g/L)',
            'chlorides': 'Хлориды (g/L)',
            'free_sulfur_dioxide': 'Свободный диоксид серы (mg/L)',
            'total_sulfur_dioxide': 'Общий диоксид серы (mg/L)',
            'density': 'Плотность (g/mL)',
            'pH': 'Уровень pH',
            'sulphates': 'Сульфаты (g/L)',
            'alcohol': 'Содержание алкоголя (%)',
            'wine_type_red': 'Тип вина (1 - красное, 0 - белое)'
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
