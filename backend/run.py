from api import create_apis

apis = create_apis()

if __name__ == '__main__':
    apis.run(host='localhost', port=3001,debug=True)
