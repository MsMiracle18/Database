import mongoengine as db

# Підключення до бази даних MongoDB
db.connect('Cluster0', host='mongodb+srv://ms_miracle18:ryPanrIWBPIoqX0T@cluster0.d6hdlvu.mongodb.net/')

# Модель для колекції "authors"
class Author(db.Document):
    name = db.StringField(required=True, max_length=100)
    birth_year = db.IntField()
    nationality = db.StringField(max_length=50)

    def __str__(self):
        return self.name

# Модель для колекції "quotes"
class Quote(db.Document):
    text = db.StringField(required=True)
    author = db.ReferenceField(Author, reverse_delete_rule=db.CASCADE)

    def __str__(self):
        return self.text

# Створення нового автора
author = Author(name='John Doe', birth_year=1980, nationality='American')
author.save()

# Створення нової цитати
quote = Quote(text='This is a sample quote.', author=author)
quote.save()
