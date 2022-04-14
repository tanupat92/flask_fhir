#!pip install fhirpy

from fhirpy import SyncFHIRClient
import dateutil.parser
import numpy as np

if __name__ == '__main__':

        client = SyncFHIRClient(
            'http://10.0.0.50:10601/fhir',
            authorization='Bearer TOKEN',
        )
        # Search for patients
        resources = client.resources('Observation')  # Return lazy search set
        resources = resources.search(subject__reference="Patient/1",
                                     code__coding="http://loinc.org|8478-0",
                                     )
        patients = resources.fetch()  # Returns list of AsyncFHIRResource
        value = patients[np.argmax([dateutil.parser.isoparse(p.effectiveDateTime) for p in patients])].valueQuantity[
            "value"]
        print(value)

