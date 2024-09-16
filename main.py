import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from who_got_money import latest_funds
from data_extractor import past_day_fundings

def send_mails():
    print("Extracting Funding Details...")
    latest_funds()
    print("Completed the extraction about the funding. Now extracting details about the specific companies...")
    past_day_fundings()

    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = Credentials.from_service_account_file('funding-bot-435820-2dbe86913a29.json', scopes=scope)
    client = gspread.authorize(creds)

    print("Uploading data to Google Sheets...")
    csv_file = 'latest_final_data.csv'
    df = pd.read_csv(csv_file)

    # Replace problematic values with None (JSON-friendly)
    df.replace([np.inf, -np.inf], None, inplace=True)
    df = df.where(pd.notnull(df), None)

    sheet = client.create('Funded Companies')
    worksheet = sheet.get_worksheet(0)
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet.id}/edit"
    emails_to_share = ['jesper@nayaone.com', 'purusharth@nayaone.com']
    print(f"Sending emails to: {', '.join(emails_to_share)}...")
    for email in emails_to_share:
        sheet.share(email, perm_type='user', role='writer')

    gmail_user = 'nayaonefundingbot@gmail.com'
    gmail_password = 'dili xirc trbp yyva'

    def send_email(to_email, sheet_url):
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to_email
        msg['Subject'] = 'Google Sheets Link'

        body = f"Here is the link to the Google Sheets: {sheet_url}"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        text = msg.as_string()
        server.sendmail(gmail_user, to_email, text)
        server.quit()

    for email in emails_to_share:
        send_email(email, sheet_url)

    print("Emails sent successfully!")

if __name__ == "__main__":
    send_mails()