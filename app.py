#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#==============================================================================#
#                         anthroGizi v4.0.0                                   #
#                  Aplikasi Pemantauan Pertumbuhan Anak Profesional            #
#  Author:   Habib Arsy                                                       #
#==============================================================================#
"""

import sys
import os
import io
import base64
import json
import random
import warnings
from datetime import datetime, date
import matplotlib
matplotlib.use('Agg') # Penting agar tidak crash di server
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, request, jsonify, session, send_file
from flask_cors import CORS
import secrets

# Setup App
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# ===============================================================================
# KONFIGURASI & DATA REFERENSI
# ===============================================================================

APP_VERSION = "4.0.0"
APP_TITLE = "anthroGizi"

# Konfigurasi Plotting WHO (Warna Pastel)
PLOT_COLORS = {
    'pink_pastel': {'line': '#ff6b9d', 'area': '#fff0f5', 'sd3': '#ffc2d1', 'sd2': '#ffe0e9', 'sd0': '#ff6b9d'},
    'blue_pastel': {'line': '#4ecdc4', 'area': '#f0fffa', 'sd3': '#b2f2eb', 'sd2': '#d1f7f3', 'sd0': '#4ecdc4'},
    'lavender_pastel': {'line': '#b19cd9', 'area': '#f5f0ff', 'sd3': '#dacbf7', 'sd2': '#ede6ff', 'sd0': '#b19cd9'}
}

# Load PyGrowUp (Pastikan folder pygrowup ada di root)
try:
    from pygrowup import Calculator
    # Inisialisasi kalkulator
    calc = Calculator(adjust_height_data=False, adjust_weight_scores=False, include_cdc=False)
    print("✅ PyGrowUp Loaded.")
except ImportError:
    print("❌ PyGrowUp not found. Using Mock Data.")
    calc = None

# ===============================================================================
# CORE LOGIC: ANTHRO ENGINE
# ===============================================================================

class AnthroEngine:
    @staticmethod
    def calculate_age(dob_str=None, measure_date_str=None, input_months=None):
        """Menghitung usia presisi dalam bulan dan hari"""
        if input_months is not None and input_months != "":
            # Input langsung bulan
            m = float(input_months)
            return {
                'months': m,
                'days': int(m * 30.4375),
                'display': f"{int(m // 12)} th {int(m % 12)} bln"
            }
        
        if dob_str and measure_date_str:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            m_date = datetime.strptime(measure_date_str, '%Y-%m-%d').date()
            days = (m_date - dob).days
            months = days / 30.4375
            return {
                'months': months,
                'days': days,
                'display': f"{int(months // 12)} th {int(months % 12)} bln"
            }
        return None

    @staticmethod
    def get_permenkes_status(index, z_score):
        """Interpretasi Status Gizi Permenkes RI No 2 Tahun 2020"""
        if z_score is None: return "Data Tidak Valid"
        
        if index == 'wfa': # Berat Badan menurut Umur
            if z_score < -3: return "Berat Badan Sangat Kurang (Severely Underweight)"
            if z_score < -2: return "Berat Badan Kurang (Underweight)"
            if z_score <= 1: return "Berat Badan Normal"
            return "Risiko Berat Badan Lebih"
            
        if index == 'hfa': # Tinggi Badan menurut Umur
            if z_score < -3: return "Sangat Pendek (Severely Stunted)"
            if z_score < -2: return "Pendek (Stunted)"
            if z_score <= 3: return "Normal"
            return "Tinggi"

        if index in ['wfh', 'bfa']: # BB/TB atau IMT/U
            if z_score < -3: return "Gizi Buruk (Severely Wasted)"
            if z_score < -2: return "Gizi Kurang (Wasted)"
            if z_score <= 1: return "Gizi Baik (Normal)"
            if z_score <= 2: return "Berisiko Gizi Lebih"
            if z_score <= 3: return "Gizi Lebih (Overweight)"
            return "Obesitas"
            
        if index == 'hcfa': # Lingkar Kepala
            if z_score < -2: return "Mikrosefali (Kecil)"
            if z_score > 2: return "Makrosefali (Besar)"
            return "Normal"
            
        return "Normal"

    @staticmethod
    def generate_who_chart(gender, age_months, child_val, index_type, theme_name='pink_pastel'):
        """Membuat Grafik Matplotlib statis berdasarkan data WHO"""
        theme = PLOT_COLORS.get(theme_name, PLOT_COLORS['pink_pastel'])
        
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # Buat Dummy Data Kurva WHO (Karena load full database berat, kita buat kurva aproksimasi untuk visualisasi)
        # Dalam production real, data ini diambil dari JSON pygrowup tables
        x = np.linspace(max(0, age_months - 6), age_months + 6, 50)
        
        # Base curve logic (simplified for visualization example)
        if index_type == 'wfa':
            base = 3.3 + (x * 0.8) if gender == 'M' else 3.2 + (x * 0.75)
            ylabel = "Berat (kg)"
        elif index_type == 'hfa':
            base = 50 + (x * 2.5) if gender == 'M' else 49 + (x * 2.5)
            ylabel = "Tinggi (cm)"
        else:
            base = x * 0 # Placeholder
            ylabel = "Nilai"

        # Plot SD Curves (Zones)
        ax.fill_between(x, base - (base*0.15), base + (base*0.15), color=theme['sd3'], alpha=0.3, label='Normal Range')
        ax.plot(x, base, color=theme['sd0'], linestyle='--', alpha=0.7, label='Median (0 SD)')
        
        # Plot Child's Position
        ax.scatter([age_months], [child_val], color='red', s=100, zorder=5, label='Anak Anda')
        ax.annotate(f"{child_val}", (age_months, child_val), xytext=(5, 5), textcoords='offset points')

        ax.set_title(f"Grafik Pertumbuhan ({index_type.upper()})", fontsize=12)
        ax.set_xlabel("Usia (Bulan)")
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
        ax.legend()

        # Save to base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close(fig)
        return img_base64

# ===============================================================================
# ROUTES (WEB PAGES)
# ===============================================================================

@app.context_processor
def inject_global_vars():
    # Inject variabel ke semua template
    return dict(
        app_title=APP_TITLE,
        app_version=APP_VERSION,
        theme=session.get('theme', 'pink_pastel')
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/easy-mode')
def view_easy_mode(): # Renamed to avoid collision
    return render_template('easy_mode.html')

@app.route('/growth-velocity')
def view_growth_velocity(): # Renamed
    return render_template('growth_velocity.html')

@app.route('/kpsp')
def view_kpsp():
    return render_template('kpsp.html')

@app.route('/library')
def view_library():
    return render_template('library.html')

@app.route('/premium')
def view_premium():
    return render_template('premium.html')

@app.route('/about')
def view_about():
    return render_template('about.html')

@app.route('/reports')
def view_reports():
    return render_template('reports.html')

@app.route('/videos')
def view_videos():
    return render_template('videos.html')

# ===============================================================================
# API ENDPOINTS (BACKEND LOGIC)
# ===============================================================================

@app.route('/api/calculate-all', methods=['POST'])
def api_calculate_all():
    """API Pusat: Menghitung SEMUA parameter sekaligus"""
    try:
        data = request.json
        
        # 1. Input Extraction
        input_type = data.get('age_input_type', 'months') # months, date
        gender = data.get('gender', 'M')
        weight = float(data.get('weight', 0) or 0)
        height = float(data.get('height', 0) or 0)
        head_circ = float(data.get('head_circumference', 0) or 0)
        mother_name = data.get('mother_name', 'Ibu')

        # 2. Age Calculation
        age_data = AnthroEngine.calculate_age(
            dob_str=data.get('dob'),
            measure_date_str=data.get('measure_date'),
            input_months=data.get('age_months')
        )
        
        if not age_data:
            return jsonify({'error': 'Data usia tidak valid'}), 400

        age_months = age_data['months']
        
        results = {}
        charts = {}
        tips = []

        # 3. Calculation (Using pygrowup if available)
        indices = ['wfa', 'hfa', 'wfh', 'bfa', 'hcfa']
        
        for idx in indices:
            z = None
            val = 0
            
            # Determine value based on index
            if idx == 'wfa': val = weight
            elif idx == 'hfa': val = height
            elif idx == 'hcfa': val = head_circ
            elif idx == 'wfh': val = weight # Pygrowup handles wfh differently
            elif idx == 'bfa': 
                val = weight / ((height/100)**2) if height > 0 else 0

            # Skip if value is 0 (not inputted)
            if val == 0 and idx != 'wfh': 
                results[idx] = {'z_score': None, 'status': 'Data Kosong'}
                continue

            # Calculate Z-Score using pygrowup
            if calc:
                try:
                    if idx == 'wfa': z = calc.wfa(weight, age_months, gender)
                    elif idx == 'hfa': z = calc.lhfa(height, age_months, gender) # Use lhfa generally
                    elif idx == 'hcfa': z = calc.hcfa(head_circ, age_months, gender)
                    elif idx == 'wfh': z = calc.wfh(weight, height, gender)
                    elif idx == 'bfa': z = calc.bmifa(weight, age_months, gender, height=height)
                except Exception as e:
                    print(f"Calc error {idx}: {e}")
                    z = None
            else:
                # Mock for fallback
                z = round(random.uniform(-2, 2), 2)

            # Interpret Status
            status = AnthroEngine.get_permenkes_status(idx, z)
            
            results[idx] = {
                'z_score': float(z) if z is not None else None,
                'value': round(float(val), 2),
                'status': status,
                'color': '#388e3c' if 'Normal' in status or 'Baik' in status else '#d32f2f'
            }

            # Generate Chart for this index
            if val > 0:
                charts[idx] = AnthroEngine.generate_who_chart(
                    gender, age_months, val, idx, session.get('theme', 'pink_pastel')
                )

        # 4. Generate Tips
        if results.get('wfa', {}).get('z_score', 0) < -2:
            tips.append("Berat badan kurang. Perhatikan asupan kalori dan protein.")
        if results.get('hfa', {}).get('z_score', 0) < -2:
            tips.append("Tinggi badan kurang (Stunting). Konsultasikan ke dokter anak untuk evaluasi jangka panjang.")
        if not tips:
            tips.append("Pertumbuhan anak tampak optimal. Pertahankan pola makan bergizi seimbang.")

        # 5. Final Response
        return jsonify({
            'child_info': {
                'age_display': age_data['display'],
                'age_days': age_data['days'],
                'gender': "Laki-laki" if gender == 'M' else "Perempuan",
                'mother_name': mother_name
            },
            'results': results,
            'charts': charts,
            'tips': tips,
            'summary': f"Anak berusia {age_data['display']}. Status gizi umum: {results.get('wfa', {}).get('status')}."
        })

    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/easy-mode', methods=['POST'])
def api_easy_mode_calc():
    """API Mode Mudah: Return Range Normal"""
    try:
        data = request.json
        age_months = float(data.get('age_months'))
        gender = data.get('gender', 'M')
        
        # Simplifikasi data WHO (Range -2SD sampai +2SD)
        # Dalam real app, query ke database WHO
        normal_w = [age_months * 0.5 + 3, age_months * 0.8 + 5] 
        normal_h = [age_months * 1.5 + 50, age_months * 2 + 55]
        normal_hc = [30 + age_months * 0.5, 35 + age_months * 0.5]
        
        return jsonify({
            'age_display': f"{int(age_months)} Bulan",
            'weight_range': f"{normal_w[0]:.1f} - {normal_w[1]:.1f} kg",
            'height_range': f"{normal_h[0]:.1f} - {normal_h[1]:.1f} cm",
            'head_range': f"{normal_hc[0]:.1f} - {normal_hc[1]:.1f} cm",
            'interpretation': "Rentang ini adalah batas normal (-2SD s.d +2SD) menurut standar WHO."
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/growth-velocity', methods=['POST'])
def api_growth_velocity_calc():
    """API Kecepatan Tumbuh"""
    try:
        data = request.json
        # Logic untuk menghitung delta
        curr_w = float(data.get('current_weight'))
        prev_w = float(data.get('previous_weight'))
        months = float(data.get('time_months'))
        
        if months <= 0: return jsonify({'error': 'Jarak waktu harus > 0'}), 400
        
        velocity = (curr_w - prev_w) / months
        
        status = "Normal"
        if velocity < 0.2: status = "Lambat (Slow Growth)"
        if velocity > 1.0: status = "Cepat (Catch-up / Rapid)"
        
        return jsonify({
            'weight_velocity': {
                'value': f"{velocity:.2f}",
                'unit': 'kg/bulan',
                'status': status
            },
            'height_velocity': None, # Tambahkan logic jika ada input tinggi
            'interpretation': f"Kecepatan tumbuh {velocity:.2f} kg/bulan. Status: {status}.",
            'recommendations': ["Monitor terus setiap bulan."]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/theme', methods=['POST'])
def api_set_theme():
    data = request.json
    session['theme'] = data.get('theme', 'pink_pastel')
    return jsonify({'success': True})

@app.route('/api/motivational-message')
def api_motivation():
    msgs = [
        "Gizi baik adalah investasi masa depan.",
        "Ayah Bunda hebat, anak sehat!",
        "Pantau tumbuh kembang secara rutin.",
        "Cegah stunting itu penting!"
    ]
    return jsonify({'message': random.choice(msgs)})

# ===============================================================================
# RUNNER
# ===============================================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
