import os
from dotenv import load_dotenv
from app import create_app, db

load_dotenv()

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Make db available in Flask shell"""
    return {'db': db}

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized.')

@app.cli.command()
def drop_db():
    """Drop all tables in the database."""
    if input('Are you sure? (y/n): ').lower() == 'y':
        db.drop_all()
        print('Database dropped.')

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])