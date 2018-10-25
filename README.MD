for fireup the server install(if you dont have them ,  they are installed in linux 
by diffult) :
    python 2.7.x
    pip
then enter this commands:
    pip install Django
    pip install djangorestframework

then go to booksRest folder and enter :
    python manage.py runserver


if you dont want to install them in  all around OS
first create virtualenv with command(Note: this need internet) :
    mkvirtualenv booksRest

then active it  by:
    source booksRest/bin/acticate

then install that requeries
(Note:when you closed the terminal and again want to start project must first
active vitualenv then fireup server)


admin username :
root

admin password :
root

auth token :
d93c0cd63d90e257bede80e1e5cc1d5060b803e0
(NOTE:Add an authorization header "Authorization:Token <your token>" when you want access to any url)

it is better to use of 'postman' but also you can use of 'curl' command

sample:
     -localhost:8000/books (get: send a list of exist books , post: create a book query)\n
     -../books/BOOK_ID (post : get a book information by its id)
     -../books/BOOK_ID/vote/ (post : vote a book)
     -../publishers/ (same with 2 but for publishers)
     -../authors/ (same with 2 but for authors)
     -../users/ (post : create user)
     -../login/ (post : make a new token for you)
