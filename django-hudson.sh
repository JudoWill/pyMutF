mkvirtualenv ve --no-site-packages
workon ve
pip install -e git://github.com/davedash/django-fixture-magic#egg=django_fixture_magic
pip install -e git://github.com/cmheisel/nose-xcover.git#egg=nosexcover
pip install -q -E ./ve -r requirements.pip
cd ./DistAnnot
python manage.py test --with-coverage --cover-package=DistAnnot --with-xunit --with-xcoverage Interaction