import os
import sqlite3
from sqlite3 import Error
from werkzeug.datastructures import FileStorage


def insert_into_database(file_path_name, file_name_blob, file_name, words, music, book, title): 
  try:
    conn = sqlite3.connect('app.db')
    conn.text_factory = str   
    print("[INFO] : Successful connection!")
    cur = conn.cursor()
    insert_file = '''INSERT INTO uploads(file_name, file_blob, words, music, book, title)
      VALUES(?, ?, ?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(insert_file, (file_name, file_name_blob, words, music, book, title ))
    conn.commit()
    print("[INFO] : The blob for ", file_path_name, " is in the database.") 
  except Error as e:
    print(e)
  finally:
    if conn:
      conn.close()
    else:
      error = "Oh shucks, something is wrong here."

def convert_into_binary(file_path):
  print("[INFO] : converting into binary data rn")
  with open(file_path, 'rb') as file:
    binary = file.read()
  return binary


def uploader(path, file_name, words, music, book, title):
  file_path_name = path
  file_name_blob = convert_into_binary(file_path_name)
  print("[INFO] : the last 100 characters of blob = ", file_name_blob[:100]) 
  insert_into_database(file_path_name, file_name_blob, file_name, words, music, book, title)


def main():
  file_path_name = input("Enter full file path:\n") 
  file_name_blob = convert_into_binary(file_path_name)
  print("[INFO] : the last 100 characters of blob = ", file_name_blob[:100]) 
  insert_into_database(file_path_name, file_name_blob)
  

if __name__ == "__main__":
  main()
