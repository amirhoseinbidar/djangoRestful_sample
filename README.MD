## requirements
  *  python 2.7.x
  *  pip
then install djano and rest framework:
    pip install Django
    pip install djangorestframework

and runserver :
    python manage.py runserver

admin username :
root

admin password :
root

auth token :
d93c0cd63d90e257bede80e1e5cc1d5060b803e0  
(NOTE:Add an authorization header "Authorization:Token [your token]" when you want access urls)

it is better use 'postman' but also you can use 'curl' command

sample:
1. localhost:8000/books (get: send a list of exist books)\n
2. ../books/BOOK_ID/ (post : get information of a book using its id)
3. ../books/BOOK_ID/vote/ (post : vote a book)
4. ../publishers/ (same with 2 but for publishers)
5. ../authors/ (same with 2 but for authors)
6. ../users/ (post : create a account )
7. ../login/ (post : make a new token for you)
