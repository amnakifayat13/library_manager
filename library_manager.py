from pymongo import MongoClient

# MongoDB Atlas connection string
connection_string = "mongodb+srv://amna:KAHM13082411*ff@cluster0.1ygdc.mongodb.net/libManager?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
client = MongoClient(connection_string)
db = client["library_db"]
collection = db["books"]

# Function to add a book
def add_book():
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    genre = input("Enter book genre: ")
    year = int(input("Enter publication year: "))
    read = input("Have you read this book? (yes/no): ").lower() == "yes"

    book = {
        "title": title,
        "author": author,
        "genre": genre,
        "year": year,
        "read": read  
    }

    collection.insert_one(book)
    print("Book added successfully!")

# Function to view all books
def view_books():
    books = collection.find()
    for book in books:
        print(book)

# Function to search for a book
def search_book():
    search_term = input("Enter title, author, or genre to search: ")
    query = {
        "$or": [
            {"title": {"$regex": search_term, "$options": "i"}},
            {"author": {"$regex": search_term, "$options": "i"}},
            {"genre": {"$regex": search_term, "$options": "i"}}
        ]
    }
    books = collection.find(query)
    for book in books:
        print(book)

# Function to update a book
def update_book():
    title = input("Enter the title of the book to update: ")
    new_title = input("Enter new title (leave blank to keep current): ")
    new_author = input("Enter new author (leave blank to keep current): ")
    new_genre = input("Enter new genre (leave blank to keep current): ")
    new_year = input("Enter new publication year (leave blank to keep current): ")
    new_read = input("Have you read this book? (yes/no, leave blank to keep current): ").lower()

    update_data = {}
    if new_title:
        update_data["title"] = new_title
    if new_author:
        update_data["author"] = new_author
    if new_genre:
        update_data["genre"] = new_genre
    if new_year:
        update_data["year"] = int(new_year)
    if new_read:
        update_data["read"] = new_read == "yes"

    collection.update_one({"title": title}, {"$set": update_data})
    print("Book updated successfully!")

# Function to delete a book
def delete_book():
    title = input("Enter the title of the book to delete: ")
    collection.delete_one({"title": title})
    print("Book deleted successfully!")

# Function to display statistics
def display_statistics():
    total_books = collection.count_documents({})  
    read_books = collection.count_documents({"read": True})  

    if total_books > 0:
        percentage_read = (read_books / total_books) * 100
    else:
        percentage_read = 0

    print("\n--- Library Statistics ---")
    print(f"Total books: {total_books}")
    print(f"Percentage of books read: {percentage_read:.2f}%")

# Main menu
def main():
    while True:
        print("\n--- Personal Library Manager ---")
        print("1. Add a book")
        print("2. View all books")
        print("3. Search for a book")
        print("4. Update a book")
        print("5. Delete a book")
        print("6. Display statistics")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            update_book()
        elif choice == "5":
            delete_book()
        elif choice == "6":
            display_statistics()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()