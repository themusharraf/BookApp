from allnc.app import AllNc

app = AllNc()


@app.route('/', allowed_methods=['get'])
def index(request, response):
    response.html = app.template('index.html')
