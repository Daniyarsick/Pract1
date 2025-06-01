#!/bin/bash

# =============================================================================
# Скрипт проверки статуса всех компонентов проекта Wine Quality ML
# =============================================================================

echo "🍷 Проверка статуса проекта Wine Quality ML"
echo "=============================================="

# Проверка файлов проекта
echo "📁 Проверка файловой структуры:"
echo "✅ README.md: $([ -f README.md ] && echo "найден" || echo "❌ отсутствует")"
echo "✅ Jupyter Notebook: $([ -f notebook/wine_quality_analysis.ipynb ] && echo "найден" || echo "❌ отсутствует")"
echo "✅ API сервис: $([ -f api/app.py ] && echo "найден" || echo "❌ отсутствует")"
echo "✅ Frontend: $([ -f frontend/app.js ] && echo "найден" || echo "❌ отсутствует")"
echo "✅ Docker конфиг: $([ -f docker/Dockerfile ] && echo "найден" || echo "❌ отсутствует")"
echo "✅ Модель: $([ -f models/best_wine_model.pkl ] && echo "найдена" || echo "❌ отсутствует")"

echo ""
echo "🔌 Проверка сервисов:"

# Проверка API сервиса
echo -n "🔗 API сервис (localhost:5001): "
if curl -s http://localhost:5001/api/health > /dev/null 2>&1; then
    echo "✅ работает"
else
    echo "❌ недоступен"
fi

# Проверка веб-приложения
echo -n "🌐 Веб-приложение (localhost:3000): "
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ работает"
else
    echo "❌ недоступен"
fi

# Проверка Docker контейнера
echo -n "🐳 Docker контейнер: "
if docker ps | grep -q wine-app; then
    echo "✅ запущен"
else
    echo "❌ не запущен"
fi

echo ""
echo "📊 Быстрый тест API:"
if curl -s http://localhost:5001/api/health > /dev/null 2>&1; then
    response=$(curl -s -X POST http://localhost:5001/api/predict \
        -H "Content-Type: application/json" \
        -d '{
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
        }')
    
    if echo "$response" | grep -q "prediction"; then
        echo "✅ Предсказание модели работает"
        echo "📈 Результат: $(echo "$response" | grep -o '"prediction":[0-9]*' | cut -d':' -f2) баллов"
    else
        echo "❌ Ошибка при предсказании"
    fi
    
    # Тест нового эндпоинта лучшего/худшего вина
    echo -n "🏆 Тест лучшего/худшего вина: "
    best_worst_response=$(curl -s http://localhost:5001/api/best-worst-wines)
    if echo "$best_worst_response" | grep -q "best_wine"; then
        echo "✅ работает"
        best_quality=$(echo "$best_worst_response" | grep -o '"quality":[0-9]*' | head -1 | cut -d':' -f2)
        worst_quality=$(echo "$best_worst_response" | grep -o '"quality":[0-9]*' | tail -1 | cut -d':' -f2)
        echo "🥇 Лучшее вино: $best_quality баллов"
        echo "🥉 Худшее вино: $worst_quality баллов"
    else
        echo "❌ не работает"
    fi
else
    echo "❌ API недоступен для тестирования"
fi

echo ""
echo "🔗 Полезные ссылки:"
echo "📊 Jupyter Notebook: notebook/wine_quality_analysis.ipynb"
echo "🔌 API документация: http://localhost:5001/api"
echo "🌐 Веб-интерфейс: http://localhost:3000"
echo "📚 GitHub: https://github.com/your-username/wine-quality-ml"

echo ""
echo "=============================================="
echo "✨ Проверка завершена!"
