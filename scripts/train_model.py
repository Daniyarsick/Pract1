import pandas as pd
import numpy as np
import joblib
import json
import os
import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Добавляем корневую директорию в путь
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from datetime import datetime

# Опциональные импорты для дополнительных алгоритмов
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    print("⚠️  XGBoost недоступен. Используем только стандартные алгоритмы sklearn.")
    XGBOOST_AVAILABLE = False

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    print("⚠️  LightGBM недоступен. Используем только стандартные алгоритмы sklearn.")
    LIGHTGBM_AVAILABLE = False

def load_and_prepare_data():
    """Загрузка и подготовка данных"""
    print("Загрузка данных...")
    
    # Загружаем данные
    data_dir = root_dir / "data"
    
    # Проверяем наличие файлов данных
    red_wine_path = data_dir / "winequality-red.csv"
    white_wine_path = data_dir / "winequality-white.csv"
    
    if not red_wine_path.exists() or not white_wine_path.exists():
        print("❌ Файлы данных не найдены в папке data/")
        print("Скачайте датасет с https://www.kaggle.com/datasets/yasserh/wine-quality-dataset")
        print("и поместите файлы winequality-red.csv и winequality-white.csv в папку data/")
        sys.exit(1)
    
    red_wine = pd.read_csv(red_wine_path, sep=';')
    white_wine = pd.read_csv(white_wine_path, sep=';')
    
    # Добавляем тип вина
    red_wine['wine_type'] = 'red'
    white_wine['wine_type'] = 'white'
    
    # Объединяем датасеты
    wine_data = pd.concat([red_wine, white_wine], ignore_index=True)
    
    # Создаем числовую версию
    wine_numeric = wine_data.copy()
    wine_numeric['wine_type_red'] = (wine_numeric['wine_type'] == 'red').astype(int)
    wine_numeric = wine_numeric.drop('wine_type', axis=1)
    
    print(f"Загружено {len(wine_data)} образцов")
    print(f"Красное вино: {len(red_wine)}, Белое вино: {len(white_wine)}")
    
    return wine_numeric

def split_data(wine_data):
    """Разделение данных на обучающую, валидационную и тестовую выборки"""
    print("Разделение данных...")
    
    X = wine_data.drop('quality', axis=1)
    y = wine_data['quality']
    
    # Стратифицированное разделение
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42, stratify=y
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.176, random_state=42, stratify=y_temp
    )
    
    print(f"Обучающая выборка: {len(X_train)} ({len(X_train)/len(X)*100:.1f}%)")
    print(f"Валидационная выборка: {len(X_val)} ({len(X_val)/len(X)*100:.1f}%)")
    print(f"Тестовая выборка: {len(X_test)} ({len(X_test)/len(X)*100:.1f}%)")
    
    return X_train, X_val, X_test, y_train, y_val, y_test

def scale_features(X_train, X_val, X_test):
    """Масштабирование признаков"""
    print("Масштабирование признаков...")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    # Преобразуем обратно в DataFrame
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
    X_val_scaled = pd.DataFrame(X_val_scaled, columns=X_val.columns, index=X_val.index)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)
    
    return X_train_scaled, X_val_scaled, X_test_scaled, scaler

def train_baseline_models(X_train, X_val, y_train, y_val):
    """Обучение baseline моделей"""
    print("\nОбучение baseline моделей...")
    
    models = {
        'DummyClassifier': DummyClassifier(strategy='most_frequent', random_state=42),
        'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000),
        'DecisionTree': DecisionTreeClassifier(random_state=42)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"  Обучение {name}...")
        model.fit(X_train, y_train)
        
        train_acc = accuracy_score(y_train, model.predict(X_train))
        val_acc = accuracy_score(y_val, model.predict(X_val))
        
        results[name] = {
            'model': model,
            'train_accuracy': train_acc,
            'val_accuracy': val_acc
        }
        
        print(f"    Val Accuracy: {val_acc:.4f}")
    
    return results

def train_advanced_models(X_train, X_val, y_train, y_val):
    """Обучение продвинутых моделей"""
    print("\nОбучение продвинутых моделей...")
    
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        'GradientBoosting': GradientBoostingClassifier(random_state=42),
        'SVM': SVC(random_state=42, probability=True),
        'KNN': KNeighborsClassifier(n_neighbors=5)
    }
    
    # Добавляем XGBoost если доступен
    if XGBOOST_AVAILABLE:
        models['XGBoost'] = xgb.XGBClassifier(random_state=42, eval_metric='mlogloss')
    
    # Добавляем LightGBM если доступен
    if LIGHTGBM_AVAILABLE:
        models['LightGBM'] = lgb.LGBMClassifier(random_state=42, verbose=-1)
    
    results = {}
    
    for name, model in models.items():
        print(f"  Обучение {name}...")
        
        try:
            model.fit(X_train, y_train)
            
            train_acc = accuracy_score(y_train, model.predict(X_train))
            val_acc = accuracy_score(y_val, model.predict(X_val))
            
            # Кросс-валидация
            cv_scores = cross_val_score(model, X_train, y_train, cv=3, scoring='accuracy')
            
            results[name] = {
                'model': model,
                'train_accuracy': train_acc,
                'val_accuracy': val_acc,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std()
            }
            
            print(f"    Val Accuracy: {val_acc:.4f} (CV: {cv_scores.mean():.4f}±{cv_scores.std():.4f})")
            
        except Exception as e:
            print(f"    Ошибка при обучении {name}: {e}")
            continue
    
    return results

def tune_best_model(best_model, model_name, X_train, y_train):
    """Тюнинг гиперпараметров лучшей модели"""
    print(f"\nТюнинг гиперпараметров для {model_name}...")
    
    if model_name == 'XGBoost' and XGBOOST_AVAILABLE:
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [3, 4, 5, 6],
            'learning_rate': [0.01, 0.1, 0.2],
            'subsample': [0.8, 0.9, 1.0],
            'colsample_bytree': [0.8, 0.9, 1.0]
        }
    elif model_name == 'RandomForest':
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
    elif model_name == 'LightGBM' and LIGHTGBM_AVAILABLE:
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.1, 0.2],
            'num_leaves': [31, 50, 100]
        }
    else:
        print(f"  Параметры для {model_name} не определены, используем базовую модель")
        return best_model
    
    # Randomized search для экономии времени
    random_search = RandomizedSearchCV(
        best_model, param_grid, n_iter=30, cv=3,
        scoring='accuracy', random_state=42, n_jobs=-1
    )
    
    random_search.fit(X_train, y_train)
    
    print(f"  Лучший CV score: {random_search.best_score_:.4f}")
    print(f"  Лучшие параметры: {random_search.best_params_}")
    
    return random_search.best_estimator_

def evaluate_final_model(model, X_test, y_test, y):
    """Финальная оценка модели"""
    print("\nФинальная оценка модели...")
    
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)
    
    test_accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba, multi_class='ovr')
    
    print(f"Точность на тестовой выборке: {test_accuracy:.4f}")
    print(f"ROC AUC (OvR): {roc_auc:.4f}")
    
    print("\nОтчет по классификации:")
    print(classification_report(y_test, y_pred))
    
    return test_accuracy, roc_auc

def save_model_and_artifacts(model, scaler, metadata, model_name):
    """Сохранение модели и артефактов"""
    print("\nСохранение модели...")
    
    # Создаем директорию для моделей
    models_dir = root_dir / "models"
    models_dir.mkdir(exist_ok=True)
    
    # Сохраняем модель и скейлер
    joblib.dump(model, models_dir / "best_wine_model.pkl")
    joblib.dump(scaler, models_dir / "scaler.pkl")
    
    # Преобразуем метаданные в JSON-сериализуемый формат
    def convert_to_serializable(obj):
        """Преобразует объекты NumPy в стандартные типы Python"""
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_to_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(convert_to_serializable(item) for item in obj)
        else:
            return obj
    
    # Применяем преобразование к метаданным
    serializable_metadata = convert_to_serializable(metadata)
    
    # Сохраняем метаданные
    with open(models_dir / "model_metadata.json", 'w') as f:
        json.dump(serializable_metadata, f, indent=2)
    
    print(f"Модель сохранена в {models_dir / 'best_wine_model.pkl'}")
    print(f"Скейлер сохранен в {models_dir / 'scaler.pkl'}")
    print(f"Метаданные сохранены в {models_dir / 'model_metadata.json'}")

def main():
    """Основная функция обучения"""
    print("=== НАЧАЛО ОБУЧЕНИЯ МОДЕЛИ ===")
    print(f"Время начала: {datetime.now()}")
    
    # Загрузка и подготовка данных
    wine_data = load_and_prepare_data()
    
    # Разделение данных
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(wine_data)
    
    # Масштабирование
    X_train_scaled, X_val_scaled, X_test_scaled, scaler = scale_features(X_train, X_val, X_test)
    
    # Обучение baseline моделей
    baseline_results = train_baseline_models(X_train_scaled, X_val_scaled, y_train, y_val)
    
    # Обучение продвинутых моделей
    advanced_results = train_advanced_models(X_train_scaled, X_val_scaled, y_train, y_val)
    
    # Выбор лучшей модели
    all_results = {**baseline_results, **advanced_results}
    best_model_name = max(all_results.keys(), key=lambda x: all_results[x]['val_accuracy'])
    best_model = all_results[best_model_name]['model']
    
    print(f"\nЛучшая модель: {best_model_name}")
    print(f"Валидационная точность: {all_results[best_model_name]['val_accuracy']:.4f}")
    
    # Тюнинг лучшей модели
    tuned_model = tune_best_model(best_model, best_model_name, X_train_scaled, y_train)
    
    # Финальная оценка
    test_accuracy, roc_auc = evaluate_final_model(tuned_model, X_test_scaled, y_test, wine_data['quality'])
    
    # Метаданные модели
    metadata = {
        'model_type': best_model_name,
        'test_accuracy': float(test_accuracy),
        'roc_auc': float(roc_auc),
        'validation_accuracy': float(all_results[best_model_name]['val_accuracy']),
        'feature_names': list(X_train.columns),
        'classes': [int(cls) for cls in sorted(wine_data['quality'].unique())],
        'training_size': int(len(X_train)),
        'features_count': int(len(X_train.columns)),
        'training_date': datetime.now().isoformat(),
        'data_shape': [int(wine_data.shape[0]), int(wine_data.shape[1])]
    }
    
    # Важность признаков (если доступна)
    if hasattr(tuned_model, 'feature_importances_'):
        feature_importance = dict(zip(X_train.columns, tuned_model.feature_importances_))
        metadata['feature_importance'] = {k: float(v) for k, v in feature_importance.items()}
    
    # Сохранение модели
    save_model_and_artifacts(tuned_model, scaler, metadata, best_model_name)
    
    print(f"\n=== ОБУЧЕНИЕ ЗАВЕРШЕНО ===")
    print(f"Время окончания: {datetime.now()}")
    print(f"Финальная точность: {test_accuracy:.4f}")

if __name__ == "__main__":
    main()
