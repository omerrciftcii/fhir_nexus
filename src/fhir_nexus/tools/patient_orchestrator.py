from typing import Dict, Any
from fhir_nexus.fhir_client import FHIRClient

class PatientDataIngestion:
    """
    Enterprise-grade engine to ingest and aggregate FHIR resources for a specific patient.
    """
    
    def __init__(self, client: FHIRClient):
        self.client = client

    def get_patient_demographics(self, patient_id: str) -> Dict[str, Any]:
        """
        Fetches patient demographic data.
        """
        print(f"Fetching demographics for patient: {patient_id}")
        return self.client.get_resource(f"Patient/{patient_id}")

    def get_patient_conditions(self, patient_id: str) -> Dict[str, Any]:
        """
        Fetches active conditions/problems for the patient.
        """
        print(f"Fetching active conditions for patient: {patient_id}")
        params = {"subject": f"Patient/{patient_id}", "clinical-status": "active"}
        return self.client.get_resource("Condition", params=params)

    def get_patient_medications(self, patient_id: str) -> Dict[str, Any]:
        """
        Fetches active medication requests for the patient.
        """
        print(f"Fetching active medications for patient: {patient_id}")
        params = {"subject": f"Patient/{patient_id}", "status": "active"}
        return self.client.get_resource("MedicationRequest", params=params)

    def get_patient_observations(self, patient_id: str) -> Dict[str, Any]:
        """
        Fetches laboratory results and vitals for the patient.
        """
        print(f"Fetching observations for patient: {patient_id}")
        params = {"subject": f"Patient/{patient_id}"}
        return self.client.get_resource("Observation", params=params)

    def aggregate_patient_record(self, patient_id: str) -> Dict[str, Any]:
        """
        Aggregates all relevant FHIR resources into a single structured clinical record.
        """
        print(f"Aggregating full clinical record for patient: {patient_id}")
        
        return {
            "demographics": self.get_patient_demographics(patient_id),
            "conditions": self.get_patient_conditions(patient_id),
            "medications": self.get_patient_medications(patient_id),
            "observations": self.get_patient_observations(patient_id)
        }