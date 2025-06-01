const express = require('express');
const path = require('path');
const axios = require('axios');
const app = express();

// Настройка Express
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Конфигурация API
const API_BASE_URL = process.env.API_URL || 'http://localhost:5000';

// Главная страница
app.get('/', (req, res) => {
    res.render('index', { 
        title: 'Wine Quality Prediction',
        result: null,
        error: null 
    });
});

// Обработка формы предсказания
app.post('/predict', async (req, res) => {
    try {
        const wineData = {
            fixed_acidity: parseFloat(req.body.fixed_acidity),
            volatile_acidity: parseFloat(req.body.volatile_acidity),
            citric_acid: parseFloat(req.body.citric_acid),
            residual_sugar: parseFloat(req.body.residual_sugar),
            chlorides: parseFloat(req.body.chlorides),
            free_sulfur_dioxide: parseFloat(req.body.free_sulfur_dioxide),
            total_sulfur_dioxide: parseFloat(req.body.total_sulfur_dioxide),
            density: parseFloat(req.body.density),
            pH: parseFloat(req.body.pH),
            sulphates: parseFloat(req.body.sulphates),
            alcohol: parseFloat(req.body.alcohol),
            wine_type_red: parseInt(req.body.wine_type_red)
        };

        // Отправка запроса к API модели
        const response = await axios.post(`${API_BASE_URL}/api/predict`, wineData, {
            headers: {
                'Content-Type': 'application/json'
            },
            timeout: 10000
        });

        res.render('index', {
            title: 'Wine Quality Prediction',
            result: response.data,
            error: null,
            inputData: req.body
        });

    } catch (error) {
        console.error('Ошибка при обращении к API:', error.message);
        
        let errorMessage = 'Ошибка при получении предсказания';
        if (error.response) {
            errorMessage = error.response.data.error || 'Ошибка сервера API';
        } else if (error.request) {
            errorMessage = 'Сервер API недоступен';
        }

        res.render('index', {
            title: 'Wine Quality Prediction',
            result: null,
            error: errorMessage,
            inputData: req.body
        });
    }
});

// API endpoint для AJAX запросов
app.post('/api/predict', async (req, res) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/api/predict`, req.body, {
            headers: {
                'Content-Type': 'application/json'
            },
            timeout: 10000
        });

        res.json(response.data);

    } catch (error) {
        console.error('Ошибка при обращении к API:', error.message);
        
        if (error.response) {
            res.status(error.response.status).json(error.response.data);
        } else {
            res.status(500).json({ error: 'Сервер API недоступен' });
        }
    }
});

// Страница с информацией об API
app.get('/api-info', (req, res) => {
    res.render('api-info', { title: 'API Information' });
});

// Проверка состояния API
app.get('/health', async (req, res) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/api/health`, {
            timeout: 5000
        });
        
        res.json({
            frontend_status: 'healthy',
            api_status: response.data,
            timestamp: new Date().toISOString()
        });
        
    } catch (error) {
        res.status(503).json({
            frontend_status: 'healthy',
            api_status: 'unavailable',
            error: error.message,
            timestamp: new Date().toISOString()
        });
    }
});

// Обработка 404
app.use((req, res) => {
    res.status(404).render('404', { title: 'Страница не найдена' });
});

// Обработка ошибок
app.use((error, req, res, next) => {
    console.error('Ошибка приложения:', error);
    res.status(500).render('error', { 
        title: 'Ошибка сервера',
        error: process.env.NODE_ENV === 'production' ? 'Внутренняя ошибка сервера' : error.message
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Frontend сервер запущен на порту ${PORT}`);
    console.log(`API URL: ${API_BASE_URL}`);
});

module.exports = app;
