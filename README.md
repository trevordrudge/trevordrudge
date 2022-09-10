# Echoes of Triumph Database
#### Video Demo: https://youtu.be/DnUmW8oUfAE
#### Description:

This project is a web database in which I can store pdf files. My grandma is a songwriter and has hundreds of songs she has written stored in a mess of folders and files in pdf format. This project is a web database where I can upload each of her song pdfs, including relevant information about each song. After each pdf is uploaded into the database, anyone who is interested in her music will easily be able to search for any song pdf that they need access to and print it from there.

All the pdf files are stored in app.db, an Sqlite3 database that stores all the pdf files as blob data. This database has only one table that also contains other relevant information such as song title, authors, and original book numbers. I debated making multiple linked tables: one to store the blob data and another for the other information, but ulitimately decided it would be simpler to keep everything in one table in the database.


At the core of this project is the main.py document. Writing the code that enabled my to convert pdfs to blob data, upload them to the database, and then retrieve them and convert them back to pdf was definately the most difficult part of this project. I ended up writing a seperate function in upload.py to take care of converting the pdfs to blob data and uploading them to the database. I call this function in main.py when i need to upload a pdf. I debated making a separate file for the retrieve pdf function, but ended up keeping it in main.py. Down the road if I develop this project further I might still move that function out of main.py because it is a rather tangly bit of code that clutters up main.py.

I have numerous html pages that make up a UI for my program. layout.html outlines the basic layout for each webpage. I use Jinja to use layout.html as a template for the rest of my pages. 

Index.html is simply the homepage for my web application. It does not include anything special.

Uploadpage.html is the page that allows me to upload pdfs to the database. in this page i chose a file, fill in the required information, and hit submit. this sends a POST request. in the python code in main.py, the post request will call the upload function and convert the pdf to blob data and upload it to the database.

Search.html is a page that allows me to search for pdfs alrady uploaded to the database. When i hit search it submits a post request that searches the database for any similar song titles. It then renders the show_results.html page with any results.

If I click on any of the results, show_pdf.html will be rendered in a new tab, displaying the pdf of the desired song.

Styles.css is the file that contains all the CSS styling code.

The wsgi.py file is the file that enables my program to run on Heroku as opposed to just running locally. If i ever further develop this project I may some day put this web application online so that the world can access my grandmas music. Unt
