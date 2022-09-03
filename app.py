import os
import sqlite3
import webbrowser
from sqlite3 import Error
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from upload import uploader




# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_EXTENSIONS'] = ['jpg', 'png', 'pdf']

Folder = os.path.join('static', 'pdfs')
app.config['RETRIEVE_FOLDER'] = Folder

Folder2 = os.path.join('static', 'Uploads')
app.config['UPLOAD_FOLDER'] = Folder2


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/show", methods=["GET", "POST"])
def show():
  # have to somehow put image into variable
  if request.method == "POST":
    pdf_id = request.form.get("pdf")

    retrieve_file(pdf_id)
    pic = os.path.join(app.config['RETRIEVE_FOLDER'], name)
    return render_template("show_pdf.html", pic=pic, name=name)
    

  else:
    return render_template("search.html")


@app.route("/search", methods=["GET", "POST"])
def search():
  # have to somehow put image into variable
  if request.method == "POST":
    pdf_id = request.form.get("pdf")

    results = search(pdf_id)
    
    return render_template("show_results.html", results = results)
  else:
    return render_template("search.html")


@app.route('/upload')
def upload_file():
   return render_template('uploadpage.html')

# Uploader        
@app.route('/uploader', methods=['GET', 'POST'])
def submitted_file():
   username = 'Trevor'
   if request.method == 'POST':
      f = request.files['file']
      if " " in f.filename:
        error = "Filename may not contain spaces"
        return render_template('uploadpage.html', username = username, error = error)
      else:
          if f and allowed_file(f.filename):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            words = request.form.get("words")
            music = request.form.get("music")
            book = request.form.get("book")
            title = request.form.get("title")
            uploader(path, f.filename, words, music, book, title)
            os.remove(path)
            return render_template('/uploadpage.html', success = f.filename)
          else:
            error = "Please upload a valid file."
            return render_template('uploadpage.html', username = username, error = error)


# checks if file name is in list in UPLOAD_EXTENSTIONS variable
def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_EXTENSIONS']

# Checks if file name has spaces



def read_blob_data(entryID):
  try:
    conn = sqlite3.connect('app.db')
    conn.text_factory = str  
    cur = conn.cursor()
    print("[INFO] : Connected to SQLite to read_blob_data")
    sql_fetch_blob_query = """SELECT * FROM uploads WHERE file_name LIKE ?"""
    cur.execute(sql_fetch_blob_query, (entryID,))
    record = cur.fetchall()
    global name
    for row in record:
      converted_file_name = row[1]
      photo_binarycode  = row[2]
      # parse out the file name from converted_file_name
      last_slash_index = converted_file_name.rfind("/") + 1 
      png_index = converted_file_name.find('.pdf')
      final_file_name = converted_file_name[last_slash_index:] 
      write_to_file(photo_binarycode, final_file_name)
      print("[DATA] : Image successfully stored on disk. Check the project directory. \n")
      print(final_file_name)
      
      name = final_file_name
    cur.close()
  except sqlite3.Error as error:
    print("[INFO] : Failed to read blob data from sqlite table", error)
  finally:
    if conn:
        conn.close()

def write_to_file(binary_data, file_name):
  Folder = os.path.join('static', 'pdfs')
  completeName = os.path.join(Folder, file_name)
  with open(completeName, 'wb') as file:
    file.write(binary_data)
  print("[DATA] : The following file has been written to file: ", file_name)

def retrieve_file(entryID):
  try:
    conn = sqlite3.connect('app.db')
    conn.text_factory = str   # added in to get rid of "u must not use 8 bit blah blah"
    print("[INFO] : Successful connection!")
    cur = conn.cursor()
    sql_retrieve_file_query = """SELECT * FROM uploads WHERE file_name = ?"""   
    cur.execute(sql_retrieve_file_query, (entryID,))
    record = cur.fetchone()
    record_blob = record   
    read_blob_data(entryID)
  except Error as e:
    print(e)
  finally:
    if conn:
      conn.close()
    else:
      error = "how did u get here." 

def search(input):
  db = SQL("sqlite:///app.db")
  rows = db.execute("SELECT file_name FROM uploads WHERE file_name LIKE ?", "%" + input + "%")

  for item in rows:
    print(item["file_name"])

  return rows




