from app import create_app
# run.py
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)