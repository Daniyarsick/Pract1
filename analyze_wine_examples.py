#!/usr/bin/env python3
"""
Анализ лучших и худших вин для создания примеров
"""

import pandas as pd
import numpy as np
import joblib
from datetime import datetime

def load_data():
    """Загрузка и объединение данных о винах"""
    print("📊 Загрузка данных...")
    
    # Загрузка красных вин
    red_wine = pd.read_csv('data/winequality-red.csv', delimiter=';')
    red_wine['wine_type_red'] = 1
    
    # Загрузка белых вин
    white_wine = pd.read_csv('data/winequality-white.csv', delimiter=';')
    white_wine['wine_type_red'] = 0
    
    # Объединение данных
    wine_data = pd.concat([red_wine, white_wine], ignore_index=True)
    
    # Стандартизация названий колонок
    wine_data.columns = [col.replace(' ', '_').lower() for col in wine_data.columns]
    
    print(f"✅ Загружено {len(wine_data)} образцов вин")
    print(f"📈 Диапазон качества: {wine_data['quality'].min()} - {wine_data['quality'].max()}")
    
    return wine_data

def analyze_quality_extremes(wine_data):
    """Анализ крайних значений качества"""
    print("\n🔍 Анализ крайних значений качества:")
    
    # Лучшие вина (8-9 баллов)
    best_wines = wine_data[wine_data['quality'] >= 8]
    print(f"🏆 Высококачественные вина (8-9 баллов): {len(best_wines)} образцов")
    
    # Худшие вина (3-4 балла)
    worst_wines = wine_data[wine_data['quality'] <= 4]
    print(f"💔 Низкокачественные вина (3-4 балла): {len(worst_wines)} образцов")
    
    # Средние вина (5-6 баллов)
    average_wines = wine_data[(wine_data['quality'] >= 5) & (wine_data['quality'] <= 6)]
    print(f"⚖️ Средние вина (5-6 баллов): {len(average_wines)} образцов")
    
    return best_wines, worst_wines, average_wines

def get_feature_statistics(best_wines, worst_wines, average_wines):
    """Получение статистики по признакам"""
    print("\n📊 Статистика признаков по группам качества:")
    
    feature_cols = ['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar',
                   'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 
                   'density', 'ph', 'sulphates', 'alcohol']
    
    stats = {}
    for group_name, group_data in [("Лучшие", best_wines), ("Худшие", worst_wines), ("Средние", average_wines)]:
        stats[group_name] = group_data[feature_cols].mean()
    
    stats_df = pd.DataFrame(stats)
    print(stats_df.round(3))
    
    return stats_df

def create_wine_examples(stats_df, wine_data):
    """Создание примеров вин на основе статистики"""
    print("\n🍷 Создание примеров вин...")
    
    # Пример лучшего красного вина (на основе средних значений лучших вин)
    best_red_wine = {
        'fixed_acidity': round(stats_df.loc['fixed_acidity', 'Лучшие'], 1),
        'volatile_acidity': round(stats_df.loc['volatile_acidity', 'Лучшие'], 2),
        'citric_acid': round(stats_df.loc['citric_acid', 'Лучшие'], 2),
        'residual_sugar': round(stats_df.loc['residual_sugar', 'Лучшие'], 1),
        'chlorides': round(stats_df.loc['chlorides', 'Лучшие'], 3),
        'free_sulfur_dioxide': round(stats_df.loc['free_sulfur_dioxide', 'Лучшие']),
        'total_sulfur_dioxide': round(stats_df.loc['total_sulfur_dioxide', 'Лучшие']),
        'density': round(stats_df.loc['density', 'Лучшие'], 4),
        'pH': round(stats_df.loc['ph', 'Лучшие'], 2),
        'sulphates': round(stats_df.loc['sulphates', 'Лучшие'], 2),
        'alcohol': round(stats_df.loc['alcohol', 'Лучшие'], 1),
        'wine_type_red': 1
    }
    
    # Пример лучшего белого вина
    best_white_wine = best_red_wine.copy()
    best_white_wine['wine_type_red'] = 0
    # Корректировка для белого вина
    best_white_wine['volatile_acidity'] = 0.25  # Белые вина обычно имеют меньше летучей кислотности
    best_white_wine['residual_sugar'] = 6.5     # Белые вина часто более сладкие
    best_white_wine['free_sulfur_dioxide'] = 35 # Больше свободного SO2
    best_white_wine['total_sulfur_dioxide'] = 140
    
    # Пример худшего красного вина
    worst_red_wine = {
        'fixed_acidity': round(stats_df.loc['fixed_acidity', 'Худшие'], 1),
        'volatile_acidity': round(stats_df.loc['volatile_acidity', 'Худшие'], 2),
        'citric_acid': round(stats_df.loc['citric_acid', 'Худшие'], 2),
        'residual_sugar': round(stats_df.loc['residual_sugar', 'Худшие'], 1),
        'chlorides': round(stats_df.loc['chlorides', 'Худшие'], 3),
        'free_sulfur_dioxide': round(stats_df.loc['free_sulfur_dioxide', 'Худшие']),
        'total_sulfur_dioxide': round(stats_df.loc['total_sulfur_dioxide', 'Худшие']),
        'density': round(stats_df.loc['density', 'Худшие'], 4),
        'pH': round(stats_df.loc['ph', 'Худшие'], 2),
        'sulphates': round(stats_df.loc['sulphates', 'Худшие'], 2),
        'alcohol': round(stats_df.loc['alcohol', 'Худшие'], 1),
        'wine_type_red': 1
    }
    
    # Пример худшего белого вина
    worst_white_wine = worst_red_wine.copy()
    worst_white_wine['wine_type_red'] = 0
    # Корректировка для белого вина
    worst_white_wine['volatile_acidity'] = 0.35
    worst_white_wine['residual_sugar'] = 12.0
    worst_white_wine['free_sulfur_dioxide'] = 25
    worst_white_wine['total_sulfur_dioxide'] = 180
    
    return {
        'best_red': best_red_wine,
        'best_white': best_white_wine,
        'worst_red': worst_red_wine,
        'worst_white': worst_white_wine
    }

def test_predictions(examples):
    """Тестирование предсказаний модели для примеров"""
    print("\n🔮 Тестирование предсказаний модели...")
    
    try:
        # Загрузка модели и скейлера
        model = joblib.load('models/best_wine_model.pkl')
        scaler = joblib.load('models/scaler.pkl')
        print("✅ Модель и скейлер загружены")
        
        results = {}
        
        for wine_type, wine_data in examples.items():
            print(f"\n🍷 Тестирование: {wine_type.replace('_', ' ').title()}")
            
            # Подготовка данных для предсказания
            features = [
                wine_data['fixed_acidity'], wine_data['volatile_acidity'], 
                wine_data['citric_acid'], wine_data['residual_sugar'],
                wine_data['chlorides'], wine_data['free_sulfur_dioxide'],
                wine_data['total_sulfur_dioxide'], wine_data['density'],
                wine_data['pH'], wine_data['sulphates'], wine_data['alcohol'],
                wine_data['wine_type_red']
            ]
            
            # Масштабирование
            features_scaled = scaler.transform([features])
            
            # Предсказание
            prediction = model.predict(features_scaled)[0]
            probabilities = model.predict_proba(features_scaled)[0]
            confidence = max(probabilities)
            
            results[wine_type] = {
                'prediction': int(prediction),
                'confidence': float(confidence),
                'probabilities': {str(i+3): float(prob) for i, prob in enumerate(probabilities)}
            }
            
            print(f"   📊 Предсказанное качество: {prediction} баллов")
            print(f"   🎯 Уверенность: {confidence:.3f}")
            print(f"   📈 Топ-3 вероятности:")
            
            # Сортировка вероятностей
            sorted_probs = sorted(results[wine_type]['probabilities'].items(), 
                                key=lambda x: x[1], reverse=True)[:3]
            for quality, prob in sorted_probs:
                if prob > 0.01:
                    print(f"      Качество {quality}: {prob:.3f}")
        
        return results
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании модели: {e}")
        return {}

def create_api_test_commands(examples):
    """Создание команд для тестирования API"""
    print("\n🔗 Команды для тестирования API:")
    
    for wine_type, wine_data in examples.items():
        print(f"\n# {wine_type.replace('_', ' ').title()}")
        print("curl -X POST http://localhost:5000/api/predict \\")
        print("  -H \"Content-Type: application/json\" \\")
        print("  -d '{")
        for key, value in wine_data.items():
            print(f'    "{key}": {value},')
        print("  }' | jq")

def save_examples_to_file(examples, results):
    """Сохранение примеров в файл"""
    print("\n💾 Сохранение примеров...")
    
    import json
    
    output = {
        'timestamp': datetime.now().isoformat(),
        'examples': examples,
        'predictions': results,
        'description': 'Примеры лучших и худших вин для тестирования модели'
    }
    
    with open('wine_examples.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print("✅ Примеры сохранены в wine_examples.json")

def main():
    """Основная функция"""
    print("🍷 АНАЛИЗ ЛУЧШИХ И ХУДШИХ ВИН")
    print("=" * 50)
    
    # Загрузка данных
    wine_data = load_data()
    
    # Анализ крайних значений
    best_wines, worst_wines, average_wines = analyze_quality_extremes(wine_data)
    
    # Статистика признаков
    stats_df = get_feature_statistics(best_wines, worst_wines, average_wines)
    
    # Создание примеров
    examples = create_wine_examples(stats_df, wine_data)
    
    # Тестирование предсказаний
    results = test_predictions(examples)
    
    # Команды для API
    create_api_test_commands(examples)
    
    # Сохранение результатов
    save_examples_to_file(examples, results)
    
    print("\n" + "=" * 50)
    print("✨ Анализ завершен! Примеры готовы для тестирования.")

if __name__ == "__main__":
    main()
