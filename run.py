#!/usr/bin/env python3
import os
from app import app

if __name__ == '__main__':
    # Mengambil port dari environment variable Render (default 5000)
    port = int(os.environ.get('PORT', 5000))
    
    # Menjalankan aplikasi
    # debug=False penting untuk production agar error tidak tampil di browser
    app.run(host='0.0.0.0', port=port, debug=False)
