from flask import Flask, render_template, request, redirect, url_for, flash
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
import driver
import Rainfall
import alerter

app = Flask(__name__, template_folder='templates')
app.secret_key = '5791628bb0b13ce0c676dfde280ba245'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/refreshFlood')
def refreshFlood():
    alerter.water_level_predictor()
    return redirect('index.html')

@app.route('/about')
def about_team():
    return render_template('about-team.html')

@app.route('/contacts')
def contact():
    return render_template('contact.html')

@app.route('/services')
def service():
    return render_template('service.html')

@app.route('/floodHome')
def floodHome():
    res = alerter.alerting()
    for i in range(len(res)):
        res[i] = 'Flood ALERT for ' + res[i]
    return render_template('flood_entry.html', result=res)

@app.route('/rainfallHome')
def rainfallHome():
    return render_template('rain_entry.html')

@app.route('/floodResult', methods=['POST', 'GET'])
def floodResult():
    if request.method == 'POST':
        if len(request.form['DATE']) == 0:
            return redirect(url_for('floodHome'))
        else:
            user_date = request.form['DATE']
            river = request.form['SEL']
            results_dict = driver.drive(river, user_date)
            Table = []
            for key, value in results_dict.items():
                Table.append(value)
            return render_template('flood_result.html', result=Table)
    else:
        return redirect(url_for('floodHome'))

@app.route('/rainfallResult', methods=['POST', 'GET'])
def rainfallResult():
    if request.method == 'POST':
        if len(request.form['Year']) == 0:
            flash("Please Enter Data!!")
            return redirect(url_for('rainfallHome'))
        else:
            year = request.form['Year']
            region = request.form['SEL']
            mae, score = Rainfall.rainfall(year, region)
            return render_template('rain_result.html', Mae=mae, Score=score)
    else:
        return redirect(url_for('rainfallHome'))

if __name__ == '__main__':
    app.run(debug=True)