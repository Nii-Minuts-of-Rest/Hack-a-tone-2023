# Hack-a-tone-2023
Анализ ответов респондентов на вопрос. (С возможностью импорта из xls и редактирования информации внутри приложения)

Запуск проекта (Сервер Debian)

git clone https://github.com/Nii-Minuts-of-Rest/Hack-a-tone-2023.git

sudo apt-get update && sudo apt-get upgrade

sudo apt install virtualenv

mkdir ~/python-environments && cd ~/python-environments

virtualenv --python=python3 env

source env/bin/activate

cd ../Hack-a-tone-2023/

pip install django
pip install pandas
pip install sklearn
pip install scikit-learn
pip install gensim
pip install nltk
pip install pymorphy2
pip install openpyxl

python manage.py migrate

python manage.py runserver 0.0.0.0:8000