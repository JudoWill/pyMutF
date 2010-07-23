cd $WORKSPACE
virtualenv -q ve
source ./ve/bin/activate
pip install -q -E ./ve -r requirements.pip
django-admin.py test --settings=DistAnnot.settings --with-coverage --cover-package=DistAnnot --with-xunit --with-xcoverage