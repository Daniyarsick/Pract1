"""
Скрипт для настройки окружения проекта Wine Quality ML
Автоматически определяет версию Python и устанавливает совместимые пакеты
"""

import sys
import subprocess
import pkg_resources
from pathlib import Path

def check_python_version():
    """Проверка версии Python и вывод рекомендаций"""
    version = sys.version_info
    print(f"Версия Python: {version.major}.{version.minor}.{version.micro}")
    
    if version >= (3, 13):
        print("⚠️  Python 3.13+ обнаружен. Некоторые пакеты могут быть несовместимы.")
        print("Рекомендуется использовать Python 3.9-3.11 для полной совместимости.")
        return "3.13+"
    elif version >= (3, 9):
        print("✅ Совместимая версия Python обнаружена.")
        return "compatible"
    else:
        print("❌ Python версии 3.9+ требуется для этого проекта.")
        return "too_old"

def install_package_safe(package_name, fallback_version=None):
    """Безопасная установка пакета с обработкой ошибок"""
    try:
        print(f"Установка {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ {package_name} установлен успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки {package_name}: {e}")
        if fallback_version:
            try:
                print(f"Попытка установки альтернативной версии: {fallback_version}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", fallback_version])
                print(f"✅ {fallback_version} установлен успешно")
                return True
            except subprocess.CalledProcessError:
                print(f"❌ Не удалось установить {fallback_version}")
        return False

def install_essential_packages():
    """Установка основных пакетов"""
    essential_packages = [
        ("pandas>=2.0.0,<3.0.0", "pandas==2.1.4"),
        ("numpy>=1.24.0,<2.0.0", "numpy==1.26.2"),
        ("scikit-learn>=1.3.0,<2.0.0", "scikit-learn==1.3.2"),
        ("flask>=2.3.0,<4.0.0", "flask==3.0.0"),
        ("flask-cors>=4.0.0", "flask-cors==4.0.0"),
        ("matplotlib>=3.7.0,<4.0.0", "matplotlib==3.8.2"),
        ("seaborn>=0.12.0,<1.0.0", "seaborn==0.13.0"),
        ("joblib>=1.3.0,<2.0.0", "joblib==1.3.2"),
        ("requests>=2.31.0,<3.0.0", "requests==2.31.0")
    ]
    
    failed_packages = []
    
    for package, fallback in essential_packages:
        if not install_package_safe(package, fallback):
            failed_packages.append(package)
    
    return failed_packages

def install_optional_packages():
    """Установка дополнительных пакетов"""
    optional_packages = [
        ("xgboost>=2.0.0", "xgboost==2.0.3"),
        ("lightgbm>=4.1.0", "lightgbm==4.1.0"),
        ("plotly>=5.15.0", "plotly==5.17.0"),
        ("jupyter>=1.0.0", "jupyter==1.0.0"),
        ("optuna>=3.2.0", "optuna==3.5.0"),
        ("shap>=0.42.0", "shap==0.43.0")
    ]
    
    print("\n=== Установка дополнительных пакетов ===")
    
    for package, fallback in optional_packages:
        install_package_safe(package, fallback)

def create_project_structure():
    """Создание структуры проекта"""
    print("\n=== Создание структуры проекта ===")
    
    directories = [
        "data",
        "models",
        "api/templates",
        "api/static",
        "frontend/views", 
        "frontend/public",
        "scripts",
        "tests",
        "notebooks/exports"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Создана директория: {directory}")

def create_gitignore():
    """Создание .gitignore файла"""
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/
.venv/
.env

# Jupyter Notebook
.ipynb_checkpoints

# Models and data
models/*.pkl
models/*.joblib
data/*.csv
data/processed/
data/raw/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Node.js (for frontend)
node_modules/
npm-debug.log*
package-lock.json

# Flask
instance/
.pytest_cache/
"""
    
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content.strip())
    
    print("📝 Создан .gitignore файл")

def main():
    """Основная функция настройки"""
    print("🍷 === НАСТРОЙКА ОКРУЖЕНИЯ WINE QUALITY ML ===\n")
    
    # Проверка версии Python
    python_status = check_python_version()
    
    if python_status == "too_old":
        print("❌ Обновите Python до версии 3.9+ и запустите скрипт снова.")
        return
    
    # Обновление pip
    print("\n=== Обновление pip ===")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ pip обновлен")
    except subprocess.CalledProcessError:
        print("⚠️  Не удалось обновить pip")
    
    # Установка setuptools и wheel
    print("\n=== Установка базовых инструментов ===")
    install_package_safe("setuptools>=65.0.0")
    install_package_safe("wheel>=0.40.0")
    
    # Установка основных пакетов
    print("\n=== Установка основных пакетов ===")
    failed = install_essential_packages()
    
    if failed:
        print(f"\n⚠️  Не удалось установить: {', '.join(failed)}")
        print("Попробуйте установить их вручную или используйте requirements-minimal.txt")
    
    # Установка дополнительных пакетов
    if python_status != "3.13+":
        install_optional_packages()
    else:
        print("\n⚠️  Пропуск дополнительных пакетов для Python 3.13+")
    
    # Создание структуры проекта
    create_project_structure()
    
    # Создание .gitignore
    create_gitignore()
    
    print("\n🎉 === НАСТРОЙКА ЗАВЕРШЕНА ===")
    print("\nДля запуска проекта:")
    print("1. Добавьте данные в папку data/")
    print("2. Запустите: python scripts/train_model.py")
    print("3. Запустите API: python api/app.py")
    print("4. Откройте http://localhost:5000 в браузере")
    
    # Проверка установленных пакетов
    print("\n=== Проверка установленных пакетов ===")
    required_packages = ['pandas', 'numpy', 'sklearn', 'flask', 'matplotlib']
    
    for package in required_packages:
        try:
            if package == 'sklearn':
                import sklearn
                print(f"✅ scikit-learn: {sklearn.__version__}")
            else:
                version = pkg_resources.get_distribution(package).version
                print(f"✅ {package}: {version}")
        except:
            print(f"❌ {package}: не установлен")

if __name__ == "__main__":
    main()
