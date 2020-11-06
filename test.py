import medacy_model_clinical_notes
model = medacy_model_clinical_notes.load()
print(model.predict("The patient was prescribed 1 capsule of Advil for 5 days."))