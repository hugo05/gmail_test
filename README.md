

Gmail API Email Processing
This project demonstrates how to use the Gmail API to fetch and process emails using Python.

How to Run
Follow these steps to configure OAuth for your Gmail client and run the scripts:

Configure OAuth

Follow the steps in the Google Developers Guide to set up OAuth for your Gmail account.
Download the credentials.json file after completing the OAuth setup.
Store Credentials

Place the credentials.json file in the root directory of this project. This file contains your OAuth credentials and is necessary for authentication.
Run Scripts

Open a terminal or command prompt.

Run the following commands in sequence:

bash
Copy code
python3 fetch_emails.py
python3 email_processing.py
These scripts will fetch emails from your Gmail account and process them according to the logic defined in email_processing.py.

