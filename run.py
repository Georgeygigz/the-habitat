#run.py

import os
from app import create_app
from instance.config import AppConfig
app = create_app(AppConfig)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
