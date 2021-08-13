import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from flask import Flask, render_template, Response
import glob
from sklearn.preprocessing import StandardScaler

def data_scaling(X_data):
    scaler=StandardScaler(with_mean=False)
    scaler.fit(X_data)
    scaled_data=scaler.transform(X_data)
    return scaled_data

app = Flask(__name__,static_folder="static",template_folder="templates")
import math

model = pickle.load(open('Final.pkl', 'rb'))

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/admin',methods=['GET'])
def admin():
    return render_template('admin.html')

@app.route('/about',methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/contact',methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/feedback',methods=['GET'])
def feedback():
    return render_template('feedback.html')

@app.route('/login',methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/reg',methods=['GET'])
def reg():
    return render_template('reg.html')


@app.route('/admin/main')
def main():
    return render_template('modified.html')

@app.route('/admin/main/y_predict',methods=['POST'])
def y_predict():
    int_features = [x for x in request.form.values()]
    print(int_features)
    final_features = [np.array(int_features)]
    final_features = data_scaling(final_features)
    prediction = model.predict(final_features)

    output = int(round(prediction[0], 2))

    return render_template('modified.html', prediction_text='Total Orders Expected For This Item: {}'.format(output))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)