import email
import imaplib
import os

# Mail Settings from my mail provider
# Incoming Server Name: imappro.zoho.com
# Port: 993
# Require SSL: Yes
# Username: you@yourdomain.com

mailUsername = "service@craigtnichols.com"
mailPort = "993"
mailServer = "imappro.zoho.com"

# Accessing my password from an environmental variable because of security

mailPassword = os.environ["mail_password"]

# Connect to email server and go to mailbox


def connect(server, username, password):
    mail = imaplib.IMAP4_SSL(mailServer)
    mail.login(username, password)
    mail.select("inbox")
    return mail


# Fetch message bodies in inbox by uid


def downloadFax(msg, uid, dir):
    type, data = msg.uid("fetch", uid, "(BODY.PEEK[])")
    email_body = data[0][1]
    mail = email.message_from_bytes(email_body)

    # Walk through multipart message

    if mail.get_content_maintype() != "multipart":
        return
    for part in mail.walk():
        # Check for attachment and specifically pdfs
        if (
            part.get_content_maintype() != "multipart"
            and part.get("Content-Disposition") is not None
            and "pdf" in part.get_filename().lower()
        ):
            # Write pdf to predefined dir
            open(dir + "/" + part.get_filename(), "wb").write(
                part.get_payload(decode=True)
            )

            # After writing copy email to "Stored" folder and mark for deletion
            msg.uid("COPY", uid, "Stored")
            msg.uid("STORE", uid, "+FLAGS", "(\Deleted)")


# Connect to mail server, grab uids for all emails in inbox to be used for reference later
def downloadAllFaxes(server, username, password, outDir):
    mail = connect(mailServer, mailUsername, mailPassword)
    result, data = mail.uid("search", None, "ALL")
    uidList = data[0].split()

    # Loop through each email
    for uid in uidList:
        downloadFax(mail, uid, outDir)

    # This is what actually deletes the email fro the inbox
    mail.expunge()


downloadAllFaxes(mailServer, mailUsername, mailPassword, "/Users/cnichols/Downloads")
