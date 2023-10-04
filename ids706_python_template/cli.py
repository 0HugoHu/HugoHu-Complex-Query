"""CLI interface for ids706_python_template project.
"""
import mysql.connector

# Create a connection to the MySQL server
connection = mysql.connector.connect(
    host="localhost", user="root", password="qwerty9870"
)

# Create a cursor to execute SQL queries
cursor = connection.cursor()

# Create a new database if it doesn't already exist
cursor.execute("CREATE DATABASE IF NOT EXISTS mydb")

# Close the cursor and the initial connection
cursor.close()
connection.close()

# Create a connection to the MySQL database
connection = mysql.connector.connect(
    host="localhost", user="root", password="qwerty9870", database="mydb"
)

# Create a cursor to execute SQL queries
cursor = connection.cursor()


def init():
    """Initialize the project."""
    # Create the authors table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS authors (
        author_id INT AUTO_INCREMENT PRIMARY KEY,
        author_name VARCHAR(255) NOT NULL
    )
    """
    )

    # Create the books table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS books (
        book_id INT AUTO_INCREMENT PRIMARY KEY,
        book_title VARCHAR(255) NOT NULL,
        author_id INT,
        FOREIGN KEY (author_id) REFERENCES authors(author_id)
    )
    """
    )

    # Create the book_loans table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS book_loans (
        loan_id INT AUTO_INCREMENT PRIMARY KEY,
        book_id INT,
        return_date DATE,
        FOREIGN KEY (book_id) REFERENCES books(book_id)
    )
    """
    )

    # Insert sample data into authors table
    cursor.execute("INSERT INTO authors (author_name) VALUES ('Author 1')")
    cursor.execute("INSERT INTO authors (author_name) VALUES ('Author 2')")

    # Insert sample data into books table
    cursor.execute(
        "INSERT INTO books (book_title, author_id) VALUES ('Book 1', 1)"
    )
    cursor.execute(
        "INSERT INTO books (book_title, author_id) VALUES ('Book 2', 1)"
    )
    cursor.execute(
        "INSERT INTO books (book_title, author_id) VALUES ('Book 3', 2)"
    )

    # Insert sample data into book_loans table
    cursor.execute(
        "INSERT INTO book_loans (book_id, return_date) VALUES (1, '2023-09-15')"
    )
    cursor.execute(
        "INSERT INTO book_loans (book_id, return_date) VALUES (2, '2023-09-20')"
    )
    cursor.execute(
        "INSERT INTO book_loans (book_id, return_date) VALUES (3, '2023-09-10')"
    )

    # Commit the changes and close the cursor and connection
    connection.commit()
    print("Tables created and sample data inserted successfully.")


def complex_query():
    # Define the SQL query
    sql_query = """
    SELECT
        authors.author_name,
        COUNT(books.book_id) AS total_books,
        MAX(loan_history.return_date) AS last_return_date
    FROM
        authors
    LEFT JOIN
        books ON authors.author_id = books.author_id
    LEFT JOIN
        book_loans AS loan_history ON books.book_id = loan_history.book_id
    GROUP BY
        authors.author_name
    ORDER BY
        last_return_date DESC;
    """

    # Execute the SQL query
    cursor.execute(sql_query)

    # Fetch all the results
    results = cursor.fetchall()

    # Close the cursor and the connection
    cursor.close()
    connection.close()

    # Process and print the results
    for row in results:
        author_name, total_books, last_return_date = row
        print(f"Author: {author_name}")
        print(f"Total Books: {total_books}")
        print(f"Last Return Date: {last_return_date}")
        print()


def main():
    init()
    complex_query()
