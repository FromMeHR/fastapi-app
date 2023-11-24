from setuptools import setup

setup(
    name='app-info',
    version='0.0.1',
    author='max',
    author_email='maxtest@gmai.com',
    description='FastAPI app',
    install_requires=[
        'fastapi==0.96.0',
        'uvicorn==0.22.0',  # server
        'SQLAlchemy==2.0.9',
        'pytest==7.4.3',
        'requests==2.28.2',
        'httpx==0.25.1',
        'PyJWT==2.8.0',
        'itsdangerous==2.1.2'
    ],
    scripts=['app/main.py', 'scripts/create_db.py']
)