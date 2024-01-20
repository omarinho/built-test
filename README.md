INSTRUCTIONS
=============

1. Copy the files into your working folder (virtual environment activation is recommended). 
2. Run `pip install -r requirements.txt` to install the dependencies.
3. Modify the config.py file with the credentials of your MySQL database. 
4. Run `flask db init`
5. Run `flask db migrate` 
6. Run `flask db upgrade`
7. Run the app (from your IDE or by executing `python app.py` in the terminal).
8. Be aware that the categories will be created in the database the first time the app is run.
