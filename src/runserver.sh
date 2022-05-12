./manage.py inspectdb --database=cran > ./index/models.py
./manage.py makemigrations index
./manage.py migrate --fake --database=cran
./manage.py runserver --database=cran
