import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///anthrogizi.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = './flask_session'
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Security configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # File upload configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'xlsx', 'csv'}
    
    # Theme configuration
    DEFAULT_THEME = 'pink_pastel'
    AVAILABLE_THEMES = {
        'pink_pastel': {
            'name': 'Pink Pastel',
            'primary': '#FF69B4',
            'secondary': '#FFB6C1',
            'accent': '#FFC0CB',
            'background': '#FFF5F8',
            'text': '#2D3748'
        },
        'blue_pastel': {
            'name': 'Blue Pastel',
            'primary': '#87CEEB',
            'secondary': '#B0E0E6',
            'accent': '#E0F6FF',
            'background': '#F0F8FF',
            'text': '#2D3748'
        },
        'lavender_pastel': {
            'name': 'Lavender Pastel',
            'primary': '#E6E6FA',
            'secondary': '#D8BFD8',
            'accent': '#DDA0DD',
            'background': '#F8F8FF',
            'text': '#2D3748'
        }
    }
    
    # WHO Configuration
    WHO_STANDARDS_FILE = 'data/who_standards.csv'
    WHO_REFERENCE_TABLES = {
        'wfa_boys': 'data/wfa_boys_p_exp.txt',
        'wfa_girls': 'data/wfa_girls_p_exp.txt',
        'hfa_boys': 'data/lhfa_boys_p_exp.txt',
        'hfa_girls': 'data/lhfa_girls_p_exp.txt',
        'wfh_boys': 'data/wfh_boys_p_exp.txt',
        'wfh_girls': 'data/wfh_girls_p_exp.txt'
    }
    
    # Premium packages configuration
    PREMIUM_PACKAGES = {
        'free': {
            'name': 'Free',
            'price': 0,
            'features': ['basic_calculator', 'limited_articles', 'basic_videos'],
            'limits': {'daily_calculations': 5, 'consultations': 0}
        },
        'silver': {
            'name': 'Silver',
            'price': 49999,
            'features': ['unlimited_calculator', 'premium_articles', 'ad_free_videos', 'basic_reports', 'whatsapp_consultation'],
            'limits': {'consultations': 2, 'report_exports': 10}
        },
        'gold': {
            'name': 'Gold',
            'price': 99999,
            'features': ['all_features', 'priority_support', 'advanced_analytics', 'unlimited_consultations', 'custom_notifications'],
            'limits': {'consultations': -1, 'report_exports': -1}
        }
    }
    
    # Notification configuration
    NOTIFICATION_INTERVAL = 20  # seconds for motivational messages
    MOTIVATIONAL_MESSAGES = [
        "Setiap anak adalah bakat istimewa yang sedang berkembang ✨",
        "Gizi yang baik hari ini adalah investasi masa depan 💪",
        "Perkembangan anak adalah perjalanan, bukan perlombaan 🌱",
        "Konsistensi dalam gizi memberikan hasil terbaik 🎯",
        "Setiap langkah kecil menuju kesehatan sangat berarti 💖",
        "Anak yang sehat adalah anak yang bahagia 😊",
        "Pertumbuhan optimal membutuhkan cinta, nutrisi, dan perhatian ❤️",
        "Anda melakukan pekerjaan luar biasa sebagai orang tua 👏",
        "Gizi seimbang kunci tumbuh kembang cerdas 🧠",
        "Hari ini adalah hari yang tepat untuk memulai kebiasaan bais 🌟"
    ]
    
    # Video content criteria
    VIDEO_MIN_SUBSCRIBERS = 10000
    VIDEO_CATEGORIES = ['nutrition', 'cooking', 'health', 'development', 'expert']
    
    # Export configuration
    EXPORT_FORMATS = ['pdf', 'excel', 'csv']
    EXPORT_MAX_RECORDS = 1000
    
    # Cache configuration
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Development configuration
    DEBUG = os.environ.get('FLASK_DEBUG') or True
    TESTING = False
    
    # Production configuration
    if os.environ.get('FLASK_ENV') == 'production':
        DEBUG = False
        TESTING = False
        SESSION_COOKIE_SECURE = True
        SESSION_COOKIE_HTTPONLY = True
        SESSION_COOKIE_SAMESITE = 'Lax'
        PERMANENT_SESSION_LIFETIME = timedelta(hours=12)

class DevelopmentConfig(Config):
    DEBUG = True
    CACHE_TYPE = 'simple'

class ProductionConfig(Config):
    DEBUG = False
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}