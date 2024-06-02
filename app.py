from allnc.app import AllNc

from auth import STATIC_TOKEN, TokenMiddleware, login_required
from storge import BookStorge

app = AllNc()
book_storge = BookStorge()
book_storge.create(name="7 Atomic Habits", author="Steven Covey")


@app.route('/', allowed_methods=['get'])
def index(request, response):
    books = book_storge.all()
    response.html = app.template('index.html', context={"books": books})


@app.route("/login", allowed_methods=["post"])
def login(request, response):
    response.json = {"token": STATIC_TOKEN}


@app.route("/books", allowed_methods=["post"])
@login_required
def create_book(request, response):
    book = book_storge.create(**request.POST)

    response.status_code = 201
    response.json = book._asdict()


@app.route("/books/{id:d}", allowed_methods=["delete"])
def delete_book(request, response, id):
    book = book_storge.delete(id)

    response.status_code = 204
