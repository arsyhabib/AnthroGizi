from app import app  # Changed from 'create_app'

if __name__ == '__main__':
    # ... keep your existing print statements ...
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
