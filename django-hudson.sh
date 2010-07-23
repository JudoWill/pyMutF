virtualenv -q ve --no-site-packages
source ./ve/bin/activate
pip install -e git://github.com/davedash/django-fixture-magic#egg=django_fixture_magic --install-dir ./ve/lib/python2.6/site-packages/
pip install -e git://github.com/cmheisel/nose-xcover.git#egg=nosexcover --install-dir ./ve/lib/python2.6/site-packages/
pip install -q -E ./ve -r requirements.pip --install-dir ./ve/lib/python2.6/site-packages/
cd ./DistAnnot
python manage.py test --with-coverage --cover-package=DistAnnot --with-xunit --with-xcoverage Interaction