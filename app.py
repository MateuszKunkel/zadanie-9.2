from flask import Flask, render_template, request
import requests
import csv

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
list_of_rates = data[0]["rates"]


def create_CSV():
    list_of_dic = []
    with open("requestedvalues.csv", "w", newline="") as csvfile:
        fieldnames = list(list_of_rates[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

        writer.writeheader()
        for i in range(0, len(list_of_rates)):
            writer.writerow(list_of_rates[i])
            list_of_dic.append(list_of_rates[i])
            
        return list_of_dic


@app.route("/", methods=["GET", "POST"])
def func():  
    input_options = create_CSV()
    last_request = ""

    if request.method == "POST":
        request_data = request.form
        waluta = request_data.get("waluta")
        ilosc = float(request_data.get("ilosc"))
        swap = waluta.split(":")

        last_request = f"Kupując {ilosc} waluty {swap[0]} zapłacisz {float(swap[1]) * ilosc} zł"

    return render_template("input.html", options = input_options, last = last_request)

if __name__ == "__main__":
    app.run(debug=True)