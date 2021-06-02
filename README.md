# GoToConnect Fax Downloader

The python script in this repo does the following:

1. It connects to a email inbox via IMAP.
2. It filters through emails and looks specifically for attachments with pdf in the name.
3. It downloads the attachments to whatever directory is configured in the script.
4. It creates a copy of the emails with the attachments we just downloaded to another folder so we don't create dupblicates
5. It deletes the original email out of the inbox
