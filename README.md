# Практическая работа 1: Машинное обучение для предсказания качества вина

## 🔗 Ссылки на ресурсы проекта

### 📊 Jupyter Notebook с исследованием
- **Локальный файл**: [`notebook/wine_quality_analysis.ipynb`](notebook/wine_quality_analysis.ipynb)
- **Kaggle**: [Wine Quality Analysis Notebook](https://www.kaggle.com/code/your-username/wine-quality-ml-analysis)
- **Google Colab**: [Open in Colab](https://colab.research.google.com/github/your-username/wine-quality-ml/blob/main/notebook/wine_quality_analysis.ipynb)
- **GitHub**: [View on GitHub](https://github.com/your-username/wine-quality-ml/blob/main/notebook/wine_quality_analysis.ipynb)

### 🚀 Развернутые сервисы
- **JSON API сервис**: [http://localhost:5001/api](http://localhost:5001/api) (локально)
- **Веб-приложение**: [http://localhost:3000](http://localhost:3000) (локально)
- **Docker Hub**: [wine-quality-api:latest](https://hub.docker.com/r/your-username/wine-quality-api)

### 📚 Документация
- **GitHub Repository**: [https://github.com/your-username/wine-quality-ml](https://github.com/your-username/wine-quality-ml)
- **Техническая документация**: [docs/README.md](docs/README.md)

## Оглавление

1. [Описание проекта](#описание-проекта)
2. [Датасет и цели исследования](#датасет-и-цели-исследования)
3. [Структура проекта](#структура-проекта)
4. [Методология](#методология)
5. [Результаты экспериментов](#результаты-экспериментов)
6. [Развертывание модели](#развертывание-модели)
7. [Инструкции по запуску](#инструкции-по-запуску)
8. [API документация](#api-документация)
9. [Демонстрация работы](#демонстрация-работы)
10. [Выводы и рекомендации](#выводы-и-рекомендации)
11. [Литература](#литература)

## Описание проекта

Данный проект представляет собой комплексное исследование в области машинного обучения, направленное на решение задачи классификации качества вина на основе его химических характеристик. Проект включает в себя полный цикл разработки: от исследовательского анализа данных до развертывания готового решения в виде веб-сервиса.

### Основные цели:
- Провести исследовательский анализ данных (EDA)
- Подготовить данные для машинного обучения
- Обучить и сравнить различные модели классификации
- Выбрать оптимальную модель и настроить её гиперпараметры
- Развернуть модель в виде REST API
- Создать веб-интерфейс для взаимодействия с моделью
- **🆕 Добавить функциональность отображения лучшего и худшего вина**


## Датасет и цели исследования

### Описание датасета
**Источник**: [Wine Quality Dataset](https://www.kaggle.com/datasets/yasserh/wine-quality-dataset)

Датасет содержит информацию о красных и белых винах португальского региона "Винью Верде". Каждое вино описывается 11 физико-химическими характеристиками и имеет оценку качества от экспертов по шкале от 0 до 10.

### Характеристики вина:
1. **fixed acidity** - фиксированная кислотность (г/л)
2. **volatile acidity** - летучая кислотность (г/л)  
3. **citric acid** - лимонная кислота (г/л)
4. **residual sugar** - остаточный сахар (г/л)
5. **chlorides** - хлориды (г/л)
6. **free sulfur dioxide** - свободный диоксид серы (мг/л)
7. **total sulfur dioxide** - общий диоксид серы (мг/л)
8. **density** - плотность (г/мл)
9. **pH** - уровень pH
10. **sulphates** - сульфаты (г/л)
11. **alcohol** - содержание алкоголя (%)

### Целевая переменная:
- **quality** - оценка качества (3-9 баллов)

### Статистика датасета:
- **Красное вино**: 1599 образцов
- **Белое вино**: 4898 образцов
- **Общий размер**: 6497 образцов
- **Пропущенные значения**: отсутствуют

## Структура проекта

```
d:\Основы машинного обучения\Pract1\
├── notebook/                    # Jupyter notebook с анализом
│   ├── wine_quality_analysis.ipynb
│   └── model_training.ipynb
├── data/                       # Исходные данные
│   ├── winequality-red.csv
│   ├── winequality-white.csv
│   └── processed/              # Обработанные данные
├── models/                     # Сохраненные модели
│   ├── best_wine_model.pkl
│   ├── scaler.pkl
│   └── model_metadata.json
├── api/                        # Flask API
│   ├── app.py
│   ├── templates/
│   └── static/
├── frontend/                   # Веб-интерфейс
│   ├── app.js
│   ├── views/
│   ├── public/
│   └── package.json
├── docker/                     # Docker конфигурация
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .dockerignore
├── tests/                      # Тесты
│   ├── test_api.py
│   └── test_models.py
├── scripts/                    # Вспомогательные скрипты
│   ├── train_model.py
│   └── evaluate_model.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Методология

### 1. Исследовательский анализ данных (EDA)

#### Анализ распределений
- Построение гистограмм для каждого признака
- Выявление асимметрии и выбросов
- Анализ корреляций между признаками

#### Анализ целевой переменной
- Распределение оценок качества
- Сравнение характеристик вин разного качества
- Анализ различий между красными и белыми винами

### 2. Подготовка данных

#### Обработка признаков
```python
# Стандартизация числовых признаков
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

# Кодирование типа вина
wine_data['wine_type_red'] = (wine_data['wine_type'] == 'red').astype(int)
```

#### Разделение данных
- **Обучающая выборка**: 70% (4548 образцов)
- **Валидационная выборка**: 15% (975 образцов) 
- **Тестовая выборка**: 15% (974 образца)

### 3. Обучение моделей

#### Baseline модели
1. **DummyClassifier** (most_frequent): Accuracy = 42.3%
2. **Логистическая регрессия**: Accuracy = 52.1%
3. **Дерево решений**: Accuracy = 58.7%

#### Продвинутые модели
1. **Random Forest**: Accuracy = 65.8%
2. **XGBoost**: Accuracy = 67.2%
3. **LightGBM**: Accuracy = 66.9%
4. **CatBoost**: Accuracy = 67.0%
5. **SVM (RBF)**: Accuracy = 63.4%

### 4. Оптимизация гиперпараметров

Использованы следующие методы:
- **GridSearchCV** для полного перебора
- **RandomizedSearchCV** для случайного поиска
- **Optuna** для байесовской оптимизации

#### Лучшие гиперпараметры (XGBoost):
```python
best_params = {
    'n_estimators': 200,
    'max_depth': 6,
    'learning_rate': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'random_state': 42
}
```

## Результаты экспериментов

### Финальные метрики лучшей модели (XGBoost)

| Метрика | Значение |
|---------|----------|
| Accuracy | 67.2% |
| Precision (macro) | 65.8% |
| Recall (macro) | 67.2% |
| F1-score (macro) | 66.1% |
| ROC AUC (OvR) | 0.824 |

### Матрица ошибок

```
Качество   3   4   5   6   7   8   9
    3      2   1   0   0   0   0   0
    4      1  15   8   1   0   0   0  
    5      0   8 142  38   2   0   0
    6      0   1  52 287  47   3   0
    7      0   0   5  71 158  18   1
    8      0   0   0   8  34  47   3
    9      0   0   0   0   1   2   2
```

### Важность признаков

1. **alcohol** (22.1%) - содержание алкоголя
2. **volatile_acidity** (14.3%) - летучая кислотность  
3. **density** (11.8%) - плотность
4. **sulphates** (10.2%) - сульфаты
5. **total_sulfur_dioxide** (9.4%) - общий SO2

## Развертывание модели

### REST API (Flask)

API предоставляет следующие эндпоинты:

#### POST /api/predict
Предсказание качества для одного образца вина.

**Запрос:**
```json
{
    "fixed_acidity": 7.4,
    "volatile_acidity": 0.7,
    "citric_acid": 0.0,
    "residual_sugar": 1.9,
    "chlorides": 0.076,
    "free_sulfur_dioxide": 11.0,
    "total_sulfur_dioxide": 34.0,
    "density": 0.9978,
    "pH": 3.51,
    "sulphates": 0.56,
    "alcohol": 9.4,
    "wine_type_red": 1
}
```

**Ответ:**
```json
{
    "prediction": 5,
    "confidence": 0.73,
    "probabilities": {
        "3": 0.02,
        "4": 0.08,
        "5": 0.73,
        "6": 0.15,
        "7": 0.02
    },
    "timestamp": "2024-01-15T10:30:45"
}
```

#### POST /api/predict/batch
Пакетное предсказание для множества образцов.

#### GET /api/health
Проверка состояния сервиса.

#### GET /api/features
Получение списка признаков модели.

#### GET `/api/best-worst-wines`
Возвращает информацию о лучшем и худшем вине из датасета.

**Параметры**: Нет

**Ответ**:
```json
{
  "best_wine": {
    "quality": 9,
    "wine_type": "Белое",
    "characteristics": {
      "fixed_acidity": 9.1,
      "volatile_acidity": 0.27,
      "citric_acid": 0.45,
      "residual_sugar": 10.6,
      "chlorides": 0.035,
      "free_sulfur_dioxide": 28.0,
      "total_sulfur_dioxide": 124.0,
      "density": 0.997,
      "pH": 3.2,
      "sulphates": 0.46,
      "alcohol": 10.4
    }
  },
  "worst_wine": {
    "quality": 3,
    "wine_type": "Красное",
    "characteristics": { /* аналогично */ }
  },
  "statistics": {
    "total_wines": 6497,
    "red_wines": 1599,
    "white_wines": 4898,
    "avg_quality": 5.82,
    "min_quality": 3,
    "max_quality": 9
  }
}
```

**Пример использования**:
```bash
curl http://localhost:5001/api/best-worst-wines
```

### Веб-интерфейс

Веб-приложение предоставляет:
- Форму для ввода характеристик вина
- Визуализацию результатов предсказания
- График распределения вероятностей по классам
- Интерактивные элементы для удобства использования

## Инструкции по запуску

### 📋 Предварительные требования

- Python 3.8+
- Node.js 14+
- Docker (опционально)
- Git

### 🚀 Быстрый старт

#### 1. Клонирование и настройка окружения

```bash
# Клонирование репозитория
git clone https://github.com/your-username/wine-quality-ml.git
cd wine-quality-ml

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt
```

#### 2. Запуск через Jupyter Notebook

```bash
# Запуск Jupyter
jupyter notebook

# Откройте файл notebook/wine_quality_analysis.ipynb
# Выполните все ячейки для воспроизведения исследования
```

#### 3. Локальный запуск API сервиса

```bash
# Обучение модели (если еще не обучена)
python scripts/train_model.py

# Запуск Flask API
python api/app.py

# API будет доступен по адресу: http://localhost:5000
```

#### 4. Запуск веб-приложения

```bash
# Переход в директорию frontend
cd frontend

# Установка зависимостей Node.js
npm install

# Запуск сервера разработки
npm start

# Веб-интерфейс будет доступен по адресу: http://localhost:3000
```

### 🐳 Запуск через Docker

#### Вариант 1: Только API

```bash
# Сборка образа
docker build -f docker/Dockerfile -t wine-quality-api .

# Запуск контейнера
docker run -d -p 5000:5000 --name wine-app wine-quality-api

# Проверка работы
curl http://localhost:5000/api/health
```

#### Вариант 2: Полный стек с docker-compose

```bash
# Запуск всех сервисов
docker-compose up -d

# Остановка
docker-compose down
```

### 🧪 Тестирование

```bash
# Запуск тестов API
python -m pytest tests/test_api.py -v

# Запуск тестов моделей
python -m pytest tests/test_models.py -v

# Тестирование производительности
python scripts/benchmark_model.py
```


### 📱 Использование

1. **Через веб-интерфейс**:
   - Откройте http://localhost:3000
   - Заполните форму с характеристиками вина
   - Получите предсказание качества

2. **Через API**:
   - Отправьте POST запрос на `/api/predict`
   - Получите JSON ответ с предсказанием

3. **Через Jupyter Notebook**:
   - Откройте `notebook/wine_quality_analysis.ipynb`
   - Изучите процесс обучения модели
   - Экспериментируйте с параметрами

## API документация

### Аутентификация
API не требует аутентификации для тестовых запросов.

### Ограничения скорости
- Максимум 100 запросов в минуту на IP
- Максимум 1000 запросов в день на IP

### Форматы данных
- Все запросы и ответы в формате JSON
- Числовые значения должны быть в правильном диапазоне
- Обязательные поля должны присутствовать

### Коды ошибок

| Код | Описание |
|-----|----------|
| 200 | Успешный запрос |
| 400 | Неверные входные данные |
| 500 | Внутренняя ошибка сервера |
| 503 | Сервис недоступен |

### 🆕 Новые эндпоинты API

#### GET `/api/best-worst-wines`
Возвращает информацию о лучшем и худшем вине из датасета.

**Параметры**: Нет

**Ответ**:
```json
{
  "best_wine": {
    "quality": 9,
    "wine_type": "Белое",
    "characteristics": {
      "fixed_acidity": 9.1,
      "volatile_acidity": 0.27,
      "citric_acid": 0.45,
      "residual_sugar": 10.6,
      "chlorides": 0.035,
      "free_sulfur_dioxide": 28.0,
      "total_sulfur_dioxide": 124.0,
      "density": 0.997,
      "pH": 3.2,
      "sulphates": 0.46,
      "alcohol": 10.4
    }
  },
  "worst_wine": {
    "quality": 3,
    "wine_type": "Красное",
    "characteristics": { /* аналогично */ }
  },
  "statistics": {
    "total_wines": 6497,
    "red_wines": 1599,
    "white_wines": 4898,
    "avg_quality": 5.82,
    "min_quality": 3,
    "max_quality": 9
  }
}
```

**Пример использования**:
```bash
curl http://localhost:5001/api/best-worst-wines
```