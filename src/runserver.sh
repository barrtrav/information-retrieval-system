./manage.py inspectdb --database=lisa > ./index/models.py
./manage.py makemigrations index
./manage.py migrate --fake --database=lisa
./manage.py runserver --database=lisa
