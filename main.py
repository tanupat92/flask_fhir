import flask
from flask import request, jsonify
import joblib
from fhirpy import SyncFHIRClient
import dateutil.parser
import numpy as np

with open("./demo_model.pkl", "rb") as f:
    model = joblib.load(f)

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def get_latest_observation_value(patient_id, code):
    '''code="http://loinc.org|8478-0"'''
    client = SyncFHIRClient(
        'http://10.0.0.50:10601/fhir',
        authorization='Bearer TOKEN',
    )
    # Search for patients
    resources = client.resources('Observation')
    resources = resources.search(subject__reference=f"Patient/{patient_id}",
                                 code__coding=code,
                                 )
    patients = resources.fetch()
    value = patients[np.argmax([dateutil.parser.isoparse(p.effectiveDateTime) for p in patients])].valueQuantity[
        "value"]
    print(value)
    return value

@app.route('/', methods=['POST'])
def predict():
    json_data = request.json
    patient_id = json_data["id"]
    if "x" in json_data.keys():
        features = json_data["x"]
    if "code" in json_data.keys():
        code = json_data["code"]
        features = get_latest_observation_value(patient_id, code=code)
    print(features)
    score = model.predict([[features]])[0][0]
    return {"result": score}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)