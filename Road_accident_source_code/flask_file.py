import os
from main import execution
from flask import Flask, render_template, request

image_folder = os.path.join('static', 'image')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = image_folder
app.debug = True

# route and function to handle the upload page
@app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        user_selected_values = request.form.getlist("accident") # Getting values given by user
        suggestion, accident_threshold_value, overall_safety = execution(user_selected_values)
        negative_value_count = sum(n < 0 for n in accident_threshold_value) # Checking total numer of negative difference values
        year_chart = os.path.join(app.config['UPLOAD_FOLDER'], 'year.png')
        fatal_accident = os.path.join(app.config['UPLOAD_FOLDER'], 'fatal_accident.png')
        irresponsibility = os.path.join(app.config['UPLOAD_FOLDER'], 'irresponsibility.png')
        print(overall_safety)
        return render_template('statistics.html', suggestion= suggestion, accident_threshold_value=accident_threshold_value , overall_safety=overall_safety, negative_value_count = negative_value_count, year_chart=year_chart, fatal_accident=fatal_accident, irresponsibility=irresponsibility)
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)

