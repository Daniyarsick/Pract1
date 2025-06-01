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
DATA_PATH_RED = 'data/winequality-red.csv'
DATA_PATH_WHITE = 'data/winequality-white.csv'

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    
    # Загрузка данных о винах
    red_wines = pd.read_csv(DATA_PATH_RED, sep=';')
    white_wines = pd.read_csv(DATA_PATH_WHITE, sep=';')
    
    # Добавляем тип вина
    red_wines['wine_type_red'] = 1
    white_wines['wine_type_red'] = 0
    
    # Объединяем данные
    all_wines = pd.concat([red_wines, white_wines], ignore_index=True)
    
    # Переименовываем колонки для соответствия модели
    column_mapping = {
        'fixed acidity': 'fixed_acidity',
        'volatile acidity': 'volatile_acidity',
        'citric acid': 'citric_acid',
        'residual sugar': 'residual_sugar',
        'free sulfur dioxide': 'free_sulfur_dioxide',
        'total sulfur dioxide': 'total_sulfur_dioxide'
    }
    all_wines = all_wines.rename(columns=column_mapping)
    
    logger.info("Модель, скейлер и данные о винах успешно загружены")
except Exception as e:
    logger.error(f"Ошибка загрузки модели или данных: {e}")
    model = None
    scaler = None
    all_wines = None

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

@app.route('/api/best-worst-wines', methods=['GET'])
def get_best_worst_wines():
    """Получение лучшего и худшего вина из датасета"""
    try:
        if all_wines is None:
            return jsonify({'error': 'Данные о винах не загружены'}), 500
        
        # Находим лучшее и худшее вино по качеству
        best_wine = all_wines.loc[all_wines['quality'].idxmax()]
        worst_wine = all_wines.loc[all_wines['quality'].idxmin()]
        
        def wine_to_dict(wine_series):
            wine_dict = wine_series.to_dict()
            return {
                'quality': int(wine_dict['quality']),
                'wine_type': 'Красное' if wine_dict['wine_type_red'] == 1 else 'Белое',
                'characteristics': {
                    'fixed_acidity': float(wine_dict['fixed_acidity']),
                    'volatile_acidity': float(wine_dict['volatile_acidity']),
                    'citric_acid': float(wine_dict['citric_acid']),
                    'residual_sugar': float(wine_dict['residual_sugar']),
                    'chlorides': float(wine_dict['chlorides']),
                    'free_sulfur_dioxide': float(wine_dict['free_sulfur_dioxide']),
                    'total_sulfur_dioxide': float(wine_dict['total_sulfur_dioxide']),
                    'density': float(wine_dict['density']),
                    'pH': float(wine_dict['pH']),
                    'sulphates': float(wine_dict['sulphates']),
                    'alcohol': float(wine_dict['alcohol'])
                }
            }
        
        # Также найдем статистику
        quality_stats = {
            'min_quality': int(all_wines['quality'].min()),
            'max_quality': int(all_wines['quality'].max()),
            'avg_quality': float(all_wines['quality'].mean()),
            'total_wines': len(all_wines),
            'red_wines': len(all_wines[all_wines['wine_type_red'] == 1]),
            'white_wines': len(all_wines[all_wines['wine_type_red'] == 0])
        }
        
        return jsonify({
            'best_wine': wine_to_dict(best_wine),
            'worst_wine': wine_to_dict(worst_wine),
            'statistics': quality_stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Ошибка при получении лучшего/худшего вина: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
