#!/usr/bin/env python3
"""
anthroGizi v4.0.0 - Child Nutrition and Growth Monitoring Platform
Main application runner with development server
"""

import os
import sys
from app import create_app
from config import config

def main():
    # Get configuration
    env = os.environ.get('FLASK_ENV', 'development')
    cfg = config.get(env, config['default'])
    
    # Create application
    app = create_app(cfg)
    
    # Print startup information
    print("=" * 60)
    print("anthroGizi v4.0.0 - Child Nutrition Platform")
    print("=" * 60)
    print(f"Environment: {env}")
    print(f"Debug Mode: {cfg.DEBUG}")
    print(f"Database: {cfg.SQLALCHEMY_DATABASE_URI}")
    print(f"Theme: {cfg.DEFAULT_THEME}")
    print("=" * 60)
    
    # Run the application
    try:
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=cfg.DEBUG,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\nShutting down anthroGizi...")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()