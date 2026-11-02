SMARTMESS - QUICK START

1. Extract the SmartMess folder to your Desktop.
2. Open .streamlit/secrets.toml in Notepad.
3. Replace REPLACE_WITH_YOUR_MYSQL_PASSWORD with the current password
   for MySQL user smartmess_app. Do not share this file publicly.
4. Open Command Prompt in the SmartMess folder.
5. Run:
      python -m streamlit run app.py
6. A browser tab should open. Click "Test MySQL Connection".

If the connection fails, check that the MySQL server is running and that
the username, password, and database name in secrets.toml are correct.

The project expects an existing MySQL database named smartmess.
