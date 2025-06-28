
from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    status = None
    error = None
    if request.method == 'POST':
        receipt_number = request.form.get('receipt')
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            url = f"https://egov.uscis.gov/casestatus/mycasestatus.do?appReceiptNum={receipt_number}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            status_div = soup.find("div", class_="rows text-center")
            status = status_div.get_text(strip=True) if status_div else "No se encontró el estatus."
        except Exception as e:
            error = "No se pudo obtener el estatus. Intenta más tarde."
    return render_template("index.html", status=status, error=error)

if __name__ == '__main__':
    app.run(debug=True)
