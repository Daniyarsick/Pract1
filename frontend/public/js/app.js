// Wine Quality Prediction Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('wineForm');
    const inputs = form.querySelectorAll('input, select');
    
    // Добавляем валидацию в реальном времени
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            validateInput(this);
        });
        
        input.addEventListener('blur', function() {
            validateInput(this);
        });
    });
    
    // Обработка отправки формы
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateForm()) {
            submitPrediction();
        }
    });
    
    // Предустановленные примеры
    const presetExamples = {
        'good-red': {
            wine_type_red: 1,
            fixed_acidity: 8.5,
            volatile_acidity: 0.4,
            citric_acid: 0.3,
            residual_sugar: 2.1,
            chlorides: 0.08,
            free_sulfur_dioxide: 15,
            total_sulfur_dioxide: 45,
            density: 0.996,
            pH: 3.3,
            sulphates: 0.65,
            alcohol: 11.5
        },
        'average-white': {
            wine_type_red: 0,
            fixed_acidity: 6.8,
            volatile_acidity: 0.3,
            citric_acid: 0.25,
            residual_sugar: 8.5,
            chlorides: 0.045,
            free_sulfur_dioxide: 30,
            total_sulfur_dioxide: 120,
            density: 0.994,
            pH: 3.2,
            sulphates: 0.45,
            alcohol: 10.5
        }
    };
    
    // Добавляем кнопки для примеров
    addExampleButtons();
    
    function validateInput(input) {
        const value = parseFloat(input.value);
        const min = parseFloat(input.min);
        const max = parseFloat(input.max);
        
        input.classList.remove('is-valid', 'is-invalid');
        
        if (input.value === '') {
            return;
        }
        
        if (input.type === 'number') {
            if (isNaN(value) || value < min || value > max) {
                input.classList.add('is-invalid');
                return false;
            } else {
                input.classList.add('is-valid');
                return true;
            }
        } else if (input.tagName === 'SELECT') {
            if (input.value === '') {
                input.classList.add('is-invalid');
                return false;
            } else {
                input.classList.add('is-valid');
                return true;
            }
        }
        
        return true;
    }
    
    function validateForm() {
        let isValid = true;
        
        inputs.forEach(input => {
            if (!validateInput(input)) {
                isValid = false;
            }
        });
        
        return isValid;
    }
    
    function submitPrediction() {
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        // Показываем загрузку
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Анализируем...';
        submitBtn.disabled = true;
        
        // Отправляем форму
        form.submit();
    }
    
    function addExampleButtons() {
        const formCard = document.querySelector('.card');
        const buttonGroup = document.createElement('div');
        buttonGroup.className = 'mb-3';
        buttonGroup.innerHTML = `
            <label class="form-label">Примеры для тестирования:</label>
            <div class="btn-group w-100" role="group">
                <button type="button" class="btn btn-outline-primary" onclick="loadExample('good-red')">
                    🍷 Хорошее красное
                </button>
                <button type="button" class="btn btn-outline-info" onclick="loadExample('average-white')">
                    🥂 Среднее белое
                </button>
                <button type="button" class="btn btn-outline-secondary" onclick="clearForm()">
                    🗑️ Очистить
                </button>
            </div>
        `;
        
        const firstInput = form.querySelector('.mb-3');
        firstInput.parentNode.insertBefore(buttonGroup, firstInput);
    }
    
    // Глобальные функции для кнопок
    window.loadExample = function(exampleType) {
        const example = presetExamples[exampleType];
        if (!example) return;
        
        Object.keys(example).forEach(key => {
            const input = form.querySelector(`[name="${key}"]`);
            if (input) {
                input.value = example[key];
                validateInput(input);
            }
        });
    };
    
    window.clearForm = function() {
        inputs.forEach(input => {
            input.value = '';
            input.classList.remove('is-valid', 'is-invalid');
        });
    };
    
    // Анимация результатов
    if (document.querySelector('.display-1')) {
        animateResult();
    }
    
    function animateResult() {
        const resultNumber = document.querySelector('.display-1');
        const progressBar = document.querySelector('.progress-bar');
        
        if (resultNumber) {
            const finalValue = parseInt(resultNumber.textContent);
            let currentValue = 0;
            
            const animation = setInterval(() => {
                currentValue += 0.1;
                resultNumber.textContent = Math.min(currentValue, finalValue).toFixed(1);
                
                if (currentValue >= finalValue) {
                    clearInterval(animation);
                    resultNumber.textContent = finalValue;
                }
            }, 50);
        }
        
        if (progressBar) {
            setTimeout(() => {
                progressBar.style.width = progressBar.style.width;
            }, 500);
        }
    }
    
    // Подсказки для полей
    addTooltips();
    
    function addTooltips() {
        const tooltips = {
            'fixed_acidity': 'Нелетучие кислоты, которые не испаряются (винная кислота)',
            'volatile_acidity': 'Летучие кислоты, в основном уксусная кислота',
            'citric_acid': 'Добавляется для свежести и кислотности',
            'residual_sugar': 'Сахар, оставшийся после брожения',
            'chlorides': 'Содержание соли в вине',
            'free_sulfur_dioxide': 'Предотвращает рост микробов и окисление',
            'total_sulfur_dioxide': 'Общее содержание SO2 (свободный + связанный)',
            'density': 'Зависит от содержания алкоголя и сахара',
            'pH': 'Кислотность вина (3-4 для большинства вин)',
            'sulphates': 'Добавка для консервации (сульфат калия)',
            'alcohol': 'Процентное содержание алкоголя'
        };
        
        Object.keys(tooltips).forEach(key => {
            const input = document.querySelector(`[name="${key}"]`);
            if (input) {
                input.setAttribute('title', tooltips[key]);
                input.setAttribute('data-bs-toggle', 'tooltip');
            }
        });
        
        // Инициализируем Bootstrap tooltips
        if (typeof bootstrap !== 'undefined') {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    }
});

// Функция для копирования JSON примера
function copyExampleJSON() {
    const example = {
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
    };
    
    navigator.clipboard.writeText(JSON.stringify(example, null, 2)).then(() => {
        alert('JSON пример скопирован в буфер обмена!');
    });
}

// Функция для загрузки данных о лучшем и худшем вине
async function loadBestWorstWines() {
    const contentDiv = document.getElementById('bestWorstWinesContent');
    
    // Показываем индикатор загрузки
    contentDiv.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Загрузка...</span>
            </div>
            <p class="mt-2">Загрузка данных о винах...</p>
        </div>
    `;
    
    try {
        const response = await fetch('/api/best-worst-wines');
        const data = await response.json();
        
        if (response.ok) {
            displayBestWorstWines(data);
        } else {
            throw new Error(data.error || 'Ошибка загрузки данных');
        }
    } catch (error) {
        console.error('Ошибка при загрузке данных о винах:', error);
        contentDiv.innerHTML = `
            <div class="alert alert-danger">
                <h6><i class="fas fa-exclamation-triangle"></i> Ошибка загрузки</h6>
                <p class="mb-0">${error.message}</p>
            </div>
        `;
    }
}

// Функция для отображения данных о лучшем и худшем вине
function displayBestWorstWines(data) {
    const contentDiv = document.getElementById('bestWorstWinesContent');
    
    const bestWine = data.best_wine;
    const worstWine = data.worst_wine;
    const stats = data.statistics;
    
    contentDiv.innerHTML = `
        <!-- Статистика -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="alert alert-info">
                    <h6><i class="fas fa-chart-bar"></i> Статистика датасета</h6>
                    <div class="row">
                        <div class="col-md-3">
                            <strong>Всего вин:</strong> ${stats.total_wines}
                        </div>
                        <div class="col-md-3">
                            <strong>Красных:</strong> ${stats.red_wines}
                        </div>
                        <div class="col-md-3">
                            <strong>Белых:</strong> ${stats.white_wines}
                        </div>
                        <div class="col-md-3">
                            <strong>Ср. качество:</strong> ${stats.avg_quality.toFixed(2)}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Лучшее и худшее вино -->
        <div class="row">
            <!-- Лучшее вино -->
            <div class="col-md-6 mb-3">
                <div class="card border-success">
                    <div class="card-header bg-success text-white">
                        <h6 class="mb-0">
                            <i class="fas fa-star"></i> Лучшее вино
                            <span class="badge bg-light text-success ms-2">Качество: ${bestWine.quality}</span>
                        </h6>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <span class="badge ${bestWine.wine_type === 'Красное' ? 'bg-danger' : 'bg-warning text-dark'} mb-2">
                                ${bestWine.wine_type === 'Красное' ? '🍷' : '🥂'} ${bestWine.wine_type} вино
                            </span>
                        </div>
                        ${renderWineCharacteristics(bestWine.characteristics)}
                        <button class="btn btn-success btn-sm mt-2" onclick="useWineAsExample(${JSON.stringify(bestWine.characteristics).replace(/"/g, '&quot;')}, ${bestWine.wine_type === 'Красное' ? 1 : 0})">
                            <i class="fas fa-copy"></i> Использовать как пример
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- Худшее вино -->
            <div class="col-md-6 mb-3">
                <div class="card border-danger">
                    <div class="card-header bg-danger text-white">
                        <h6 class="mb-0">
                            <i class="fas fa-thumbs-down"></i> Худшее вино
                            <span class="badge bg-light text-danger ms-2">Качество: ${worstWine.quality}</span>
                        </h6>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <span class="badge ${worstWine.wine_type === 'Красное' ? 'bg-danger' : 'bg-warning text-dark'} mb-2">
                                ${worstWine.wine_type === 'Красное' ? '🍷' : '🥂'} ${worstWine.wine_type} вино
                            </span>
                        </div>
                        ${renderWineCharacteristics(worstWine.characteristics)}
                        <button class="btn btn-danger btn-sm mt-2" onclick="useWineAsExample(${JSON.stringify(worstWine.characteristics).replace(/"/g, '&quot;')}, ${worstWine.wine_type === 'Красное' ? 1 : 0})">
                            <i class="fas fa-copy"></i> Использовать как пример
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Функция для отображения характеристик вина
function renderWineCharacteristics(characteristics) {
    const labels = {
        'fixed_acidity': 'Фиксированная кислотность',
        'volatile_acidity': 'Летучая кислотность',
        'citric_acid': 'Лимонная кислота',
        'residual_sugar': 'Остаточный сахар',
        'chlorides': 'Хлориды',
        'free_sulfur_dioxide': 'Свободный SO₂',
        'total_sulfur_dioxide': 'Общий SO₂',
        'density': 'Плотность',
        'pH': 'pH',
        'sulphates': 'Сульфаты',
        'alcohol': 'Алкоголь'
    };
    
    let html = '<div class="row">';
    let count = 0;
    
    for (const [key, value] of Object.entries(characteristics)) {
        if (count % 2 === 0 && count > 0) {
            html += '</div><div class="row">';
        }
        
        html += `
            <div class="col-6 mb-2">
                <small class="text-muted">${labels[key] || key}</small><br>
                <strong>${typeof value === 'number' ? value.toFixed(3) : value}</strong>
            </div>
        `;
        count++;
    }
    
    html += '</div>';
    return html;
}

// Функция для использования характеристик вина как примера
function useWineAsExample(characteristics, wineType) {
    // Заполняем форму характеристиками выбранного вина
    document.querySelector('[name="wine_type_red"]').value = wineType;
    
    for (const [key, value] of Object.entries(characteristics)) {
        const input = document.querySelector(`[name="${key}"]`);
        if (input) {
            input.value = value;
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
    }
    
    // Прокручиваем к форме
    document.querySelector('#wineForm').scrollIntoView({ behavior: 'smooth' });
    
    // Показываем уведомление
    const toast = `
        <div class="toast align-items-center text-white bg-primary border-0 position-fixed top-0 end-0 m-3" style="z-index: 9999;" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-check-circle me-2"></i>
                    Характеристики вина загружены в форму!
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', toast);
    const toastElement = document.querySelector('.toast:last-child');
    const bsToast = new bootstrap.Toast(toastElement, { delay: 3000 });
    bsToast.show();
    
    // Удаляем toast после закрытия
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

// Загружаем данные о лучшем и худшем вине при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Загружаем данные через небольшую задержку для лучшего UX
    setTimeout(loadBestWorstWines, 500);
});
