#!/bin/bash
virtualenv ve --no-site-packages
source ./ve/bin/activate
pip install -e git://github.com/davedash/django-fixture-magic#egg=django_fixture_magic
pip install -e git://github.com/cmheisel/nose-xcover.git#egg=nosexcover
pip install -q -E ./ve -r requirements.pip
wget http://nltk.googlecode.com/files/nltk-2.0b8.tar.gz
tar xf nltk-2.0b8.tar.gz
pip install -e nltk-2.0b8/

cd ./DistAnnot
python manage.py test --with-coverage --cover-package=DistAnnot --with-xunit --with-xcoverage