#!/bin/bash

export FN_AUTH_REDIRECT_URI=http://localhost:8040/google/auth
export FN_BASE_URI=http://localhost:8040
export FN_CLIENT_ID=
export FN_CLIENT_SECRET=

export FLASK_APP=app.py
export FLASK_DEBUG=1
export FN_FLASK_SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'

python3 -m flask run -p 8040