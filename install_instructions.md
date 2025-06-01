# Инструкции по установке Wine Quality ML

## Проблемы с Python 3.13

Если вы используете Python 3.13, некоторые пакеты могут быть несовместимы. Вот несколько способов решения:

### Вариант 1: Автоматическая настройка (Рекомендуется)

```bash
python setup_environment.py
```

### Вариант 2: Минимальная установка

```bash
pip install -r requirements-minimal.txt
```

### Вариант 3: Пошаговая установка

1. **Обновите инструменты:**
```bash
pip install --upgrade pip setuptools wheel
```

2. **Установите основные пакеты:**
```bash
pip install pandas==2.1.4 numpy==1.26.2 scikit-learn==1.3.2
```

3. **Установите веб-фреймворк:**
```bash
pip install flask==3.0.0 flask-cors==4.0.0
```

4. **Установите визуализацию:**
```bash
pip install matplotlib==3.8.2 seaborn==0.13.0
```

5. **Установите ML пакеты:**
```bash
pip install xgboost==2.0.3 joblib==1.3.2
```

### Вариант 4: Использование conda

```bash
conda create -n wine-ml python=3.11
conda activate wine-ml
conda install pandas numpy scikit-learn matplotlib seaborn flask
pip install xgboost flask-cors joblib
```

### Вариант 5: Docker (без установки зависимостей)

```bash
docker build -t wine-quality-api .
docker run -p 5000:5000 wine-quality-api
```

## Решение конкретных проблем

### Ошибка "AttributeError: module 'pkgutil' has no attribute 'ImpImporter'"

Эта ошибка связана с Python 3.13. Решения:

1. **Используйте Python 3.11 или 3.12**
2. **Обновите setuptools:**
```bash
pip install --upgrade setuptools>=69.0.0
```

3. **Установите пакеты по одному:**
```bash
pip install --no-build-isolation pandas
pip install --no-build-isolation scikit-learn
```

### Проблемы с XGBoost

```bash
# Для Windows
pip install xgboost==2.0.3

# Для Linux/Mac
conda install -c conda-forge xgboost
```

### Проблемы с LightGBM

```bash
# Альтернативная установка
pip install --prefer-binary lightgbm
```

## Проверка установки

После установки запустите:

```python
python -c "import pandas, numpy, sklearn, flask, matplotlib; print('Все основные пакеты установлены!')"
```

## Минимальные требования

Для базовой функциональности достаточно:
- pandas
- numpy  
- scikit-learn
- flask
- matplotlib
- joblib

Остальные пакеты опциональны и добавляют дополнительную функциональность.
