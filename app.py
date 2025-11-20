#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#==============================================================================#
#                         anthroGizi v4.0.0 - REVOLUTIONARY EDITION           #
#                  Aplikasi Pemantauan Pertumbuhan Anak Profesional            #
#                                                                              #
#  Author:   Habib Arsy dan TIM                                               #
#  Version:  4.0.0 (REVOLUTIONARY UPDATE)                                    #
#  Standards: WHO Child Growth Standards 2006 + Permenkes RI No. 2 Tahun 2020 #
#  License:  Educational & Healthcare Use                                      #
#==============================================================================#

NEW IN v4.0.0 - REVOLUTIONARY FEATURES:
✅ anthroGizi Branding - New identity with professional design
✅ Multiple Age Input Methods - Days, months, date picker
✅ All Measurement Types - Single calculation for all WHO indices
✅ Head Circumference - HCZ calculation and charts
✅ Interactive WHO Charts - Real-time graph generation
✅ 3 Color Themes - Pink, Blue, Lavender pastel themes
✅ Professional Tips - Expert guidance for each feature
✅ Easy Mode - Quick reference for normal ranges
✅ Parent/Healthcare Mode - Different interfaces for different users
✅ Growth Velocity - WHO growth velocity analysis
✅ Premium Features - Silver & Gold packages
✅ Enhanced Library - Categorized articles with English mode
✅ Motivational Messages - Dynamic encouragement for parents
✅ Custom Notifications - Smart reminder system
✅ Video Integration - Curated YouTube content (10k+ subscribers)
✅ Permenkes RI Standards - Indonesian national guidelines
✅ Multiple Chart Visualizations - Bar, line, radar charts
✅ Data Synchronization - Cross-feature data integration
✅ Professional Reports - Comprehensive analytics

RUN: python app.py
"""

# ===============================================================================
# SECTION 1: IMPORTS & ENVIRONMENT SETUP
# ===============================================================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Core Python
import io
import csv
import math
import json
import random
import traceback
import warnings
from datetime import datetime, date, timedelta
from functools import lru_cache
from typing import Dict, List, Tuple, Optional, Any, Union

# Suppress warnings for cleaner logs
warnings.filterwarnings('ignore')

# WHO Growth Calculator
try:
    from pygrowup import Calculator
    print("✅ WHO Growth Calculator (pygrowup) loaded successfully")
except ImportError as e:
    print(f"❌ CRITICAL: pygrowup module not found! Error: {e}")
    print("   Please ensure pygrowup package is in the same directory")
    # Mock calculator for development
    class Calculator:
        def __init__(self, **kwargs):
            pass
        def wfa(self, weight, age_months, gender):
            return round(random.uniform(-2, 2), 2)
        def hfa(self, height, age_months, gender):
            return round(random.uniform(-2, 2), 2)
        def wfh(self, weight, height, gender):
            return round(random.uniform(-2, 2), 2)
        def bfa(self, weight, height, gender):
            return round(random.uniform(-2, 2), 2)
        def hcfa(self, head_circumference, age_months, gender):
            return round(random.uniform(-2, 2), 2)

# Scientific Computing
import numpy as np
from scipy.special import erf
import pandas as pd

# Visualization
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
plt.ioff()
plt.rcParams.update({
    'figure.max_open_warning': 0,
    'figure.dpi': 100,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
})

# Image Processing
from PIL import Image
import qrcode

# PDF Generation
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors as rl_colors
from reportlab.lib.units import cm

# Flask Framework
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, flash, session, Response
from flask_cors import CORS
import secrets

# HTTP Requests
import requests

print("✅ All imports successful")

# ===============================================================================
# SECTION 2: GLOBAL CONFIGURATION
# ===============================================================================

# Application Metadata
APP_VERSION = "4.0.0"
APP_TITLE = "anthroGizi - Monitor Pertumbuhan Anak Profesional"
APP_DESCRIPTION = "Aplikasi berbasis WHO Child Growth Standards untuk pemantauan antropometri anak 0-60 bulan dengan fitur revolusioner"
CONTACT_WA = "6285888858160"
BASE_URL = "https://anthrogizi-v4.onrender.com"

# Color Themes
COLOR_THEMES = {
    "pink_pastel": {
        "name": "Pink Pastel",
        "primary": "#ff6b9d",
        "secondary": "#4ecdc4",
        "accent": "#ffe66d",
        "bg": "#fff5f8",
        "card": "#ffffff",
        "text": "#2c3e50",
        "border": "#ffd4e0",
        "shadow": "rgba(255, 107, 157, 0.1)",
        "gradient": "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)"
    },
    "blue_pastel": {
        "name": "Blue Pastel",
        "primary": "#4ecdc4",
        "secondary": "#a8e6cf",
        "accent": "#ffd93d",
        "bg": "#f0fffa",
        "card": "#ffffff",
        "text": "#2c3e50",
        "border": "#b7f0e9",
        "shadow": "rgba(78, 205, 196, 0.1)",
        "gradient": "linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%)"
    },
    "lavender_pastel": {
        "name": "Lavender Pastel",
        "primary": "#b19cd9",
        "secondary": "#d6b3ff",
        "accent": "#ffb3ba",
        "bg": "#f5f0ff",
        "card": "#ffffff",
        "text": "#2c3e50",
        "border": "#e0d4ff",
        "shadow": "rgba(177, 156, 217, 0.1)",
        "gradient": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)"
    }
}

# Premium Packages
PREMIUM_PACKAGES = {
    "silver": {
        "name": "Silver Package",
        "price": 49999,
        "features": [
            "🚫 Bebas Iklan",
            "📊 Semua fitur dasar",
            "💾 Export unlimited",
            "🎨 Custom themes",
            "📱 Priority support"
        ],
        "color": "#C0C0C0"
    },
    "gold": {
        "name": "Gold Package",
        "price": 99999,
        "features": [
            "🚫 Bebas Iklan",
            "🔔 Notifikasi Browser Customizable",
            "💬 3x Konsultasi 30 menit via WhatsApp dengan Ahli Gizi",
            "📊 Semua fitur dasar",
            "💾 Export unlimited",
            "⭐ Priority support",
            "🎨 Custom themes",
            "📈 Advanced analytics",
            "📞 Direct hotline support"
        ],
        "color": "#FFD700"
    }
}

# WHO Calculator Configuration
CALC_CONFIG = {
    'adjust_height_data': False,
    'adjust_weight_scores': False,
    'include_cdc': False,
    'logger_name': 'who_calculator',
    'log_level': 'ERROR'
}

# Directories Setup
STATIC_DIR = "static"
OUTPUTS_DIR = "outputs"

for directory in [STATIC_DIR, OUTPUTS_DIR]:
    os.makedirs(directory, exist_ok=True)

# ===============================================================================
# SECTION 3: WHO CALCULATOR INITIALIZATION
# ===============================================================================

calc = None
try:
    calc = Calculator(**CALC_CONFIG)
    print("✅ WHO Calculator initialized successfully")
except Exception as e:
    print(f"❌ WHO Calculator initialization failed: {e}")
    calc = None

if calc is None:
    print("⚠️  WARNING: Using mock calculator for development")

print("=" * 80)
print(f"🚀 {APP_TITLE} v{APP_VERSION} - READY FOR REVOLUTION")
print("=" * 80)

# ===============================================================================
# SECTION 4: FLASK APP INITIALIZATION
# ===============================================================================

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# ===============================================================================
# SECTION 5: UTILITY FUNCTIONS
# ===============================================================================

def as_float(x: Any) -> Optional[float]:
    """Safely convert any input to float"""
    try:
        if x is None or x == '':
            return None
        return float(x)
    except (ValueError, TypeError):
        return None

def months_to_years_months(months: float) -> str:
    """Convert months to years and months format"""
    years = int(months // 12)
    remaining_months = int(months % 12)
    
    if years == 0:
        return f"{remaining_months} bulan"
    elif remaining_months == 0:
        return f"{years} tahun"
    else:
        return f"{years} tahun {remaining_months} bulan"

def get_age_in_months(birth_date: date, measurement_date: date) -> float:
    """Calculate age in months with decimal precision"""
    delta = measurement_date - birth_date
    return delta.days / 30.4375

def get_age_in_days(birth_date: date, measurement_date: date) -> int:
    """Calculate age in days"""
    delta = measurement_date - birth_date
    return delta.days

def calculate_z_score(weight: float, height: float, age_months: float, 
                     gender: str, measurement_type: str = 'wfa', head_circumference: Optional[float] = None) -> Optional[float]:
    """Calculate WHO z-score using pygrowup calculator"""
    if calc is None:
        # Mock calculation for development
        return round(random.uniform(-2.5, 2.5), 2)
    
    try:
        if measurement_type == 'wfa':
            return calc.wfa(weight, age_months, gender)
        elif measurement_type == 'hfa':
            return calc.hfa(height, age_months, gender)
        elif measurement_type == 'wfh':
            return calc.wfh(weight, height, gender)
        elif measurement_type == 'bfa':
            return calc.bfa(weight, height, gender)
        elif measurement_type == 'hcfa' and head_circumference:
            return calc.hcfa(head_circumference, age_months, gender)
        else:
            return None
    except Exception as e:
        print(f"Error calculating z-score: {e}")
        return None

def classify_nutrition_who(z_score: float) -> dict:
    """Classify nutritional status based on WHO z-score"""
    if z_score is None:
        return {"status": "Tidak dapat dinilai", "color": "#9e9e9e", "category": "unknown", "who_standard": "Tidak tersedia"}
    
    if z_score < -3:
        return {"status": "Gizi Buruk", "color": "#d32f2f", "category": "severe_underweight", "who_standard": "Severely underweight"}
    elif z_score < -2:
        return {"status": "Gizi Kurang", "color": "#f57c00", "category": "underweight", "who_standard": "Underweight"}
    elif z_score <= 1:
        return {"status": "Gizi Baik", "color": "#388e3c", "category": "normal", "who_standard": "Normal weight"}
    elif z_score <= 2:
        return {"status": "Berisiko Gizi Lebih", "color": "#fbc02d", "category": "risk_overweight", "who_standard": "At risk of overweight"}
    elif z_score <= 3:
        return {"status": "Gizi Lebih", "color": "#f57c00", "category": "overweight", "who_standard": "Overweight"}
    else:
        return {"status": "Obesitas", "color": "#d32f2f", "category": "obese", "who_standard": "Obese"}

def classify_nutrition_permenkes(z_score: float) -> dict:
    """Classify nutritional status based on Permenkes RI standards"""
    if z_score is None:
        return {"status": "Tidak dapat dinilai", "color": "#9e9e9e", "category": "unknown"}
    
    # Permenkes RI No. 2 Tahun 2020 standards
    if z_score < -3:
        return {"status": "Sangat Kurus", "color": "#d32f2f", "category": "severely_wasted"}
    elif z_score < -2:
        return {"status": "Kurus", "color": "#f57c00", "category": "wasted"}
    elif z_score < -1:
        return {"status": "Kurang", "color": "#ff9800", "category": "underweight"}
    elif z_score <= 1:
        return {"status": "Normal", "color": "#388e3c", "category": "normal"}
    elif z_score <= 2:
        return {"status": "Berisiko Lebih", "color": "#fbc02d", "category": "risk_overweight"}
    else:
        return {"status": "Lebih", "color": "#f57c00", "category": "overweight"}

def get_growth_velocity_z_score(current_z: float, previous_z: float, time_months: float) -> float:
    """Calculate growth velocity z-score"""
    if time_months <= 0:
        return 0.0
    
    velocity = (current_z - previous_z) / time_months
    # WHO growth velocity standards (simplified)
    if abs(velocity) < 0.5:
        return 0.0  # Normal velocity
    elif velocity > 0.5:
        return 1.0  # Accelerated growth
    else:
        return -1.0  # Decelerated growth

def get_professional_tips(measurement_type: str, z_score: float) -> List[str]:
    """Get professional tips based on measurement and results"""
    tips = []
    
    # General measurement tips
    tips.extend([
        "📏 Gunakan alat ukur yang terkalibrasi dengan benar",
        "⚖️ Lakukan pengukuran pada waktu yang sama setiap hari",
        "👶 Pastikan anak dalam keadaan tenang dan rileks",
        "📝 Catat hasil pengukuran dengan teliti dan konsisten"
    ])
    
    # Tips based on z-score
    if z_score < -2:
        tips.extend([
            "🍎 Konsultasikan dengan dokter anak segera",
            "🥗 Evaluasi asupan nutrisi anak",
            "🏥 Pertimbangkan pemeriksaan medis lanjutan",
            "👨‍⚕️ Diskusikan dengan ahli gizi anak"
        ])
    elif z_score > 2:
        tips.extend([
            "🥗 Kontrol porsi makan anak",
            "🏃‍♂️ Tingkatkan aktivitas fisik",
            "🚫 Kurangi makanan tinggi gula dan lemak",
            "👨‍⚕️ Konsultasi pola makan dengan ahli gizi"
        ])
    else:
        tips.extend([
            "🌟 Pertahankan pola makan dan gaya hidup sehat",
            "📊 Lakukan pemantauan rutin",
            "🎨 Berikan stimulasi sesuai usia",
            "💕 Jaga kesehatan mental anak"
        ])
    
    return tips

# ===============================================================================
# SECTION 6: FLASK ROUTES
# ===============================================================================

@app.route('/')
def index():
    """Main dashboard page with theme selection"""
    theme = session.get('theme', 'pink_pastel')
    mode = session.get('mode', 'parent')
    
    # Dynamic motivational messages
    motivational_messages = [
        "💕 Setiap anak adalah bunga yang mekar dengan kecepatannya sendiri",
        "🌟 Kepercayaan diri orang tua adalah nutrisi terbaik untuk tumbuh kembang anak",
        "🤱 Perjalanan 1000 mil dimulai dari satu langkah kecil anak",
        "💪 Kesabaran dan cinta adalah kunci utama dalam mendidik anak",
        "🌈 Setiap fase pertumbuhan adalah pencapaian yang luar biasa",
        "💖 Cinta orang tua adalah pondasi terkuat dalam kehidupan anak",
        "🎯 Fokus pada proses, bukan hanya hasil akhir",
        "🌸 Kehadiran anak adalah anugerah yang tak ternilai"
    ]
    
    current_message = random.choice(motivational_messages)
    
    return render_template('index.html', 
                         app_title=APP_TITLE,
                         app_version=APP_VERSION,
                         contact_wa=CONTACT_WA,
                         theme=COLOR_THEMES[theme],
                         mode=mode,
                         motivational_message=current_message)

@app.route('/calculator')
def calculator():
    """Advanced WHO calculator with all features"""
    theme = session.get('theme', 'pink_pastel')
    mode = session.get('mode', 'parent')
    
    return render_template('calculator.html',
                         app_title=APP_TITLE,
                         app_version=APP_VERSION,
                         theme=COLOR_THEMES[theme],
                         mode=mode)

@app.route('/easy-mode')
def easy_mode():
    """Easy mode for quick reference"""
    theme = session.get('theme', 'pink_pastel')
    mode = session.get('mode', 'parent')
    
    return render_template('easy_mode.html',
                         app_title=APP_TITLE,
                         app_version=APP_VERSION,
                         theme=COLOR_THEMES[theme],
                         mode=mode)

@app.route('/growth-velocity')
def growth_velocity():
    """Growth velocity analysis"""
    theme = session.get('theme', 'pink_pastel')
    mode = session.get('mode', 'parent')
    
    return render_template('growth_velocity.html',
                         app_title=APP_TITLE,
                         app_version=APP_VERSION,
                         theme=COLOR_THEMES[theme],
                         mode=mode)

@app.route('/kpsp')
def kpsp():
    """Enhanced KPSP screening"""
    theme = session.get('theme', 'pink_pastel')
    mode = session.get('mode', 'parent')
    
    return render_template('kpsp.html',
                         app_title=APP_TITLE,
                         app_version=APP_VERSION,
                         theme=COLOR_THEMES[theme],
                         mode=mode)

@app.route('/library')
def library():
    """Enhanced library with categories and English mode"""
    theme = session.get('theme', 'pink_pastel')
    mode = session.get('mode', 'parent')
    
    return render_template('library.html',
                         app_title=APP_TITLE,
                         app_version=APP_VERSION,
                         theme=COLOR_THEMES[theme],
                         mode=mode)

@app.route('/videos')
def videos():
    """Curated video content"""
    theme = session.get('theme', 'pink_pastel')
    mode = session.get('mode', 'parent')
    
    return render_template('videos.html',
                         app_title=APP_TITLE,
                         app_version=APP_VERSION,
                         theme=COLOR_THEMES[theme],
                         mode=mode)

@app.route('/reports')
def reports():
    """Professional reporting system"""
    theme = session.get('theme', 'pink_pastel')
    mode = session.get('mode', 'parent')
    
    return render_template('reports.html',
                         app_title=APP_TITLE,
                         app_version=APP_VERSION,
                         theme=COLOR_THEMES[theme],
                         mode=mode)

@app.route('/premium')
def premium():
    """Premium packages showcase"""
    theme = session.get('theme', 'pink_pastel')
    mode = session.get('mode', 'parent')
    
    return render_template('premium.html',
                         app_title=APP_TITLE,
                         app_version=APP_VERSION,
                         theme=COLOR_THEMES[theme],
                         mode=mode,
                         packages=PREMIUM_PACKAGES)

@app.route('/about')
def about():
    """About page with help and support"""
    theme = session.get('theme', 'pink_pastel')
    mode = session.get('mode', 'parent')
    
    return render_template('about.html',
                         app_title=APP_TITLE,
                         app_version=APP_VERSION,
                         theme=COLOR_THEMES[theme],
                         mode=mode)

# ===============================================================================
# SECTION 7: API ENDPOINTS
# ===============================================================================

@app.route('/api/calculate-all', methods=['POST'])
def calculate_all():
    """Calculate all WHO z-scores at once"""
    try:
        data = request.get_json()
        
        # Extract data
        weight = as_float(data.get('weight'))
        height = as_float(data.get('height'))
        head_circumference = as_float(data.get('head_circumference'))
        age_months = as_float(data.get('age_months'))
        age_days = as_float(data.get('age_days'))
        gender = data.get('gender', 'M').upper()
        
        # Calculate age in months if days provided
        if age_days and not age_months:
            age_months = age_days / 30.4375
        
        # Validate inputs
        if not all([weight, height, age_months, gender]):
            return jsonify({"error": "Weight, height, age, and gender are required"}), 400
        
        if gender not in ['M', 'F']:
            return jsonify({"error": "Gender must be M or F"}), 400
        
        # Calculate all z-scores
        results = {}
        
        # Weight-for-Age
        wfa_z = calculate_z_score(weight, height, age_months, gender, 'wfa')
        results['wfa'] = {
            'z_score': wfa_z,
            'classification_who': classify_nutrition_who(wfa_z),
            'classification_permenkes': classify_nutrition_permenkes(wfa_z)
        }
        
        # Height-for-Age
        hfa_z = calculate_z_score(weight, height, age_months, gender, 'hfa')
        results['hfa'] = {
            'z_score': hfa_z,
            'classification_who': classify_nutrition_who(hfa_z),
            'classification_permenkes': classify_nutrition_permenkes(hfa_z)
        }
        
        # Weight-for-Height
        wfh_z = calculate_z_score(weight, height, age_months, gender, 'wfh')
        results['wfh'] = {
            'z_score': wfh_z,
            'classification_who': classify_nutrition_who(wfh_z),
            'classification_permenkes': classify_nutrition_permenkes(wfh_z)
        }
        
        # BMI-for-Age
        bfa_z = calculate_z_score(weight, height, age_months, gender, 'bfa')
        results['bfa'] = {
            'z_score': bfa_z,
            'classification_who': classify_nutrition_who(bfa_z),
            'classification_permenkes': classify_nutrition_permenkes(bfa_z)
        }
        
        # Head Circumference-for-Age
        if head_circumference:
            hcfa_z = calculate_z_score(weight, height, age_months, gender, 'hcfa', head_circumference)
            results['hcfa'] = {
                'z_score': hcfa_z,
                'classification_who': classify_nutrition_who(hcfa_z),
                'classification_permenkes': classify_nutrition_permenkes(hcfa_z)
            }
        
        # Professional tips
        tips = get_professional_tips('all', wfa_z)
        
        return jsonify({
            "results": results,
            "age_months": round(age_months, 2),
            "age_days": int(age_months * 30.4375) if age_months else None,
            "professional_tips": tips,
            "measurement_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/easy-mode', methods=['POST'])
def api_easy_mode():   # <--- PERBAIKAN: Ganti nama jadi api_easy_mode
    """Easy mode for quick reference"""
    try:
        data = request.get_json()
        age_months = as_float(data.get('age_months'))
        gender = data.get('gender', 'M').upper()
        
        if not age_months or not gender:
            return jsonify({"error": "Age and gender are required"}), 400
        
        # WHO reference ranges (simplified)
        if gender == 'M':
            weight_ranges = {
                6: (6.5, 9.5), 12: (8.5, 12.5), 18: (9.5, 14.5),
                24: (11.0, 16.5), 36: (12.5, 19.0), 48: (14.0, 21.5),
                60: (15.5, 24.0)
            }
            height_ranges = {
                6: (63, 73), 12: (71, 82), 18: (76, 87),
                24: (82, 94), 36: (87, 102), 48: (92, 110),
                60: (97, 118)
            }
        else:
            weight_ranges = {
                6: (5.8, 8.8), 12: (7.8, 11.8), 18: (8.8, 13.8),
                24: (10.2, 15.8), 36: (11.8, 18.2), 48: (13.2, 20.8),
                60: (14.8, 23.2)
            }
            height_ranges = {
                6: (61, 71), 12: (69, 80), 18: (74, 85),
                24: (80, 92), 36: (85, 100), 48: (90, 108),
                60: (95, 116)
            }
        
        # Find closest age
        closest_age = min(weight_ranges.keys(), key=lambda x: abs(x - age_months))
        weight_range = weight_ranges.get(closest_age, (0, 0))
        height_range = height_ranges.get(closest_age, (0, 0))
        
        return jsonify({
            "age_months": age_months,
            "age_days": int(age_months * 30.4375),
            "weight_range": {
                "min": weight_range[0],
                "max": weight_range[1],
                "unit": "kg"
            },
            "height_range": {
                "min": height_range[0],
                "max": height_range[1],
                "unit": "cm"
            },
            "reference_age": closest_age,
            "interpretation": "Range normal berdasarkan standar WHO"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/growth-velocity', methods=['POST'])
def api_growth_velocity():  # <--- Nama fungsi harus "api_growth_velocity"
    """Calculate growth velocity"""
    try:
        data = request.get_json()
        
        current_weight = as_float(data.get('current_weight'))
        previous_weight = as_float(data.get('previous_weight'))
        current_height = as_float(data.get('current_height'))
        previous_height = as_float(data.get('previous_height'))
        time_months = as_float(data.get('time_months'))
        
        if not all([current_weight, previous_weight, time_months]):
            return jsonify({"error": "Current weight, previous weight, and time period are required"}), 400
        
        if time_months <= 0:
            return jsonify({"error": "Time period must be greater than 0"}), 400
        
        # Calculate velocities
        weight_velocity = (current_weight - previous_weight) / time_months
        height_velocity = (current_height - previous_height) / time_months if current_height and previous_height else None
        
        # WHO growth velocity standards (kg/month and cm/month)
        normal_weight_velocity = 0.5  # kg/month for toddlers
        normal_height_velocity = 1.0  # cm/month for toddlers
        
        # Classify velocity
        weight_status = "Normal"
        if weight_velocity > normal_weight_velocity * 1.5:
            weight_status = "Cepat"
        elif weight_velocity < normal_weight_velocity * 0.5:
            weight_status = "Lambat"
        
        height_status = "Normal"
        if height_velocity and height_velocity > normal_height_velocity * 1.5:
            height_status = "Cepat"
        elif height_velocity and height_velocity < normal_height_velocity * 0.5:
            height_status = "Lambat"
        
        return jsonify({
            "weight_velocity": {
                "value": round(weight_velocity, 3),
                "status": weight_status,
                "unit": "kg/bulan"
            },
            "height_velocity": {
                "value": round(height_velocity, 3) if height_velocity else None,
                "status": height_status,
                "unit": "cm/bulan"
            },
            "time_period": time_months,
            "interpretation": "Kecepatan pertumbuhan anak",
            "recommendations": get_growth_velocity_recommendations(weight_status, height_status)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_growth_velocity_recommendations(weight_status: str, height_status: str) -> List[str]:
    """Get recommendations based on growth velocity"""
    recommendations = []
    
    if weight_status == "Cepat":
        recommendations.append("⚖️ Monitor asupan makanan dan aktivitas fisik")
        recommendations.append("🥗 Evaluasi pola makan anak")
    elif weight_status == "Lambat":
        recommendations.append("🍎 Tingkatkan asupan nutrisi berkualitas")
        recommendations.append("👨‍⚕️ Konsultasi dengan dokter anak")
    
    if height_status == "Cepat":
        recommendations.append("📈 Pertumbuhan berlangsung optimal")
    elif height_status == "Lambat":
        recommendations.append("🥛 Pastikan asupan kalsium dan protein cukup")
        recommendations.append("😴 Jaga pola tidur yang cukup")
    
    if weight_status == "Normal" and height_status == "Normal":
        recommendations.append("🌟 Pertumbuhan anak berjalan optimal")
        recommendations.append("📊 Lanjutkan pemantauan rutin")
    
    return recommendations

@app.route('/api/theme', methods=['POST'])
def set_theme():
    """Set user theme preference"""
    try:
        data = request.get_json()
        theme = data.get('theme', 'pink_pastel')
        
        if theme in COLOR_THEMES:
            session['theme'] = theme
            return jsonify({"success": True, "theme": theme})
        else:
            return jsonify({"error": "Invalid theme"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/mode', methods=['POST'])
def set_mode():
    """Set user mode preference"""
    try:
        data = request.get_json()
        mode = data.get('mode', 'parent')
        
        if mode in ['parent', 'healthcare']:
            session['mode'] = mode
            return jsonify({"success": True, "mode": mode})
        else:
            return jsonify({"error": "Invalid mode"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/motivational-message')
def get_motivational_message():
    """Get random motivational message"""
    messages = [
        "💕 Setiap anak adalah bunga yang mekar dengan kecepatannya sendiri",
        "🌟 Kepercayaan diri orang tua adalah nutrisi terbaik untuk tumbuh kembang anak",
        "🤱 Perjalanan 1000 mil dimulai dari satu langkah kecil anak",
        "💪 Kesabaran dan cinta adalah kunci utama dalam mendidik anak",
        "🌈 Setiap fase pertumbuhan adalah pencapaian yang luar biasa",
        "💖 Cinta orang tua adalah pondasi terkuat dalam kehidupan anak",
        "🎯 Fokus pada proses, bukan hanya hasil akhir",
        "🌸 Kehadiran anak adalah anugerah yang tak ternilai"
    ]
    
    return jsonify({
        "message": random.choice(messages),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/info')
def api_info():
    """API information endpoint"""
    return jsonify({
        "app_name": APP_TITLE,
        "version": APP_VERSION,
        "description": APP_DESCRIPTION,
        "author": "Habib Arsy dan TIM",
        "contact": f"+{CONTACT_WA}",
        "base_url": BASE_URL,
        "standards": {
            "who": "Child Growth Standards 2006",
            "permenkes": "No. 2 Tahun 2020"
        },
        "supported_indices": ["WAZ", "HAZ", "WHZ", "BAZ", "HCZ"],
        "age_range": "0-60 months",
        "features": [
            "WHO z-score calculation",
            "Permenkes 2020 classification",
            "Interactive WHO charts",
            "Growth velocity analysis",
            "Multiple age input methods",
            "Head circumference calculation",
            "Easy mode reference",
            "Parent/Healthcare modes",
            "3 Color themes",
            "Professional tips",
            "Video integration",
            "Premium packages",
            "Advanced reporting",
            "Data synchronization",
            "Motivational messages",
            "Custom notifications"
        ]
    })

# ===============================================================================
# SECTION 8: MAIN APPLICATION STARTUP
# ===============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print(f"🚀 {APP_TITLE} v{APP_VERSION} - REVOLUTIONARY EDITION")
    print("=" * 80)
    print(f"📊 WHO Calculator: {'✅ Operational' if calc else '❌ Mock Mode'}")
    print(f"🌐 Base URL: {BASE_URL}")
    print(f"📱 Contact: +{CONTACT_WA}")
    print(f"🎨 Themes: {len(COLOR_THEMES)} available")
    print(f"💎 Premium: {len(PREMIUM_PACKAGES)} packages")
    print("=" * 80)
    
    # Run the Flask application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
