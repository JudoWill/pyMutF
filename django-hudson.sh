cd $WORKSPACE/DistAnnot
virtualenv -q ve
source ./ve/bin/activate
pip install -q -E ./ve -r requirements.pip
python manage.py test --with-coverage --cover-package=DistAnnot --with-xunit --with-xcoverage Interaction