"""
This module is to run full application.

It includes app from app
"""
from app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
