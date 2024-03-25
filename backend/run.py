from api import create_app

api = create_app()

if __name__ == '__main__':
    api.run(debug=api.config['DEBUG'], port=api.config['PORT'], host=api.config['HOST'])
