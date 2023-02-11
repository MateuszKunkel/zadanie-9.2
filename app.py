from flask import Flask, render_template, request
import requests
import csv

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()


with open('requestedvalues.csv', 'w', newline='') as csvfile:
    fieldnames = ["currency", "code", "bid", "ask"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

    writer.writeheader()
    for i in range(0, len(data[0]["rates"])):

        writer.writerow(data[0]["rates"][i])


@app.route('/mypage/calculator', methods=['GET', 'POST'])
def func():
    last_request = 0

    if request.method == "POST":
        request_data = request.form
        waluta = request_data.get("waluta")
        ilosc = int(request_data.get("ilosc"))

        for i in range(0, len(data[0]["rates"])):
            if data[0]["rates"][i]["code"] == waluta:
                print(data[0]["rates"][i]["ask"] * ilosc)
                last_request = data[0]["rates"][i]["ask"] * ilosc
        
        return f"przelicznik waluty wyniósł {last_request} zł"

    #elif request.method == "GET":
    return render_template("example.html")
    


