class Library():
    dict ={"python":4,"DSA":2}
    def __init__(self,book_name,no_books):
        self.book_name= book_name
        self.no_books= no_books
        Library.dict[self.book_name]=self.no_books

class Check():
    def __init__(self,book):
        self.book=book
        a = Library.dict[self.book] 
        if(a==0):
            print("Book is not avalable")
        else:
            print("book is avalable")

class Get():
    def __init__(self,book):
        self.book= book
        a =int(Library.dict[self.book])
        Library.dict[self.book]=a-1
        print("your book is issued")
while(True):
        

    a = int(input("\n\nfor adding a book press 1\nfor checking book press 2\nfor get book press 3\nget all book information press 4\n"))
    if(a==1):


        book = input("enter the book name\n")
        num = int(input("enter how many book you want to add\n"))
        Library(book,num)
    elif(a==2) :
       try:
           book = input("enter the book name\n")
           Check(book)
       except:
           print("book is not avalable")
    elif(a==3) :
        try:

           book = input("enter the book name\n")
           Get(book)
        except:
            print("book is not avalable")
    elif(a==4):
        print(Library.dict)
        print("\n")
    else :
        print("enter valid number")

