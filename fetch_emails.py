from db import DB

from utils import Utils
from email_action import EmailAction

def main():

    email_data = EmailAction.fetch_emails()
    for email in email_data:
        query = "INSERT INTO Emails (id, sender, body, date, recipients, subject) VALUES (?, ?, ?, ?, ?, ?)";
        data = (email.get("id"), email.get("sender"), email.get("body"), 
            email.get("date"), email.get("recipients"), email.get("subject"))
        
        inserted = DB.insert_data(query, data)
        if inserted:
            print("Emails : {} inserted into db.".format(email.get("id")))
    
        



if __name__ == "__main__":
    main()