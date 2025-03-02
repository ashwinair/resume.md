# fetch_doc.py
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime

# Configuration
CREDS_FILE = 'credentials.json'  # Will be created by GitHub Actions
DOC_ID = 'your-document-id-here'  # Replace with your Google Doc ID

def get_doc_content():
    creds = Credentials.from_service_account_file(CREDS_FILE)
    service = build('docs', 'v1', credentials=creds)
    doc = service.documents().get(documentId=DOC_ID).execute()
    
    # Build HTML content with formatting
    html_content = ''
    for element in doc.get('body').get('content'):
        if 'paragraph' in element:
            style = element['paragraph'].get('paragraphStyle', {}).get('namedStyleType', '')
            text = ''
            for text_run in element['paragraph']['elements']:
                if 'textRun' in text_run:
                    content = text_run['textRun']['content'].strip()
                    if content:
                        if text_run['textRun'].get('textStyle', {}).get('bold'):
                            text += f'<b>{content}</b>'
                        elif text_run['textRun'].get('textStyle', {}).get('underline'):
                            text += f'<u>{content}</u>'
                        else:
                            text += content

            if not text:
                continue
                
            # Apply retro formatting based on style
            if style.startswith('HEADING_1'):
                html_content += f'<h2><u>{text}</u></h2>\n'
            elif style.startswith('HEADING_2'):
                html_content += f'<h3>{text}</h3>\n'
            elif element['paragraph'].get('bullet'):
                html_content += f'<li>{text}</li>\n'
            else:
                html_content += f'<p>{text}</p>\n'

    # Wrap in retro HTML structure
    today = datetime.now().strftime('%B %d, %Y')
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>My Resume - Retro Style</title>
    <link rel="stylesheet" href="style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <table width="100%" border="0">
        <tr>
            <td bgcolor="#000080">
                <h1><font color="#FFFFFF">Ashwin S Nair's Resume</font></h1>
            </td>
        </tr>
        <tr>
            <td bgcolor="#C0C0C0">
                <hr>
                {html_content}
                <hr>
                <p align="center">
                    Last Updated: {today}<br>
                    Best viewed in Netscape Navigator
                </p>
            </td>
        </tr>
    </table>
</body>
</html>
"""
    with open('index.html', 'w') as f:
        f.write(full_html)

if __name__ == '__main__':
    get_doc_content()
