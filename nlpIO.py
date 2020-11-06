
from medacy.model.model import Model
import medacy_model_clinical_notes
import json
import mysql.connector
import subprocess

class NLPUnit:
    def processRequest(self, js):
        #method to tokenize a string inputted from a json object
        #present in an http request.
        model = medacy_model_clinical_notes.load()
        json_data = js
        free_text = json_data['Comments']
        pid = json_data['PID']
        free_quoted = "\"" + free_text + "\""
        attributes = {'P_ID':pid, 'Drug':'NULL', 'Strength':'NULL', 'Duration':'NULL', 'Route':'NULL', 'Form':'NULL', 'ADE':'NULL', 'Dosage':'NULL', 'Reason':'NULL', 'Frequency':'NULL', 'Note': free_quoted}
        for i in model.predict(free_text):
            attributes[i.tag] = i.text
        #for i in attributes.keys():
        #    attributes[i] = "\"" + attributes[i] + "\""
        cnx = mysql.connector.connect(user='root', password='aksjhs',
                              host='localhost',
                              database='clinical')
        cur = cnx.cursor()
        add_data = ("INSERT INTO clinical_notes "
                    "(P_ID, LoggedDate, Drug, Strength, Duration, Route, Form, ADE, Dosage, Reason, Frequency, Note) "
                    "VALUES (%(P_ID)s, CURDATE(), %(Drug)s, %(Strength)s, %(Duration)s, %(Route)s, %(Form)s, %(ADE)s, %(Dosage)s, %(Reason)s, %(Frequency)s, %(Note)s)")
        cur.execute(add_data, attributes)
        
        return json.dumps(str(model.predict(free_text)))

    def processQuery(self, js):
        #method to process an NL query and convert to SQL, respond with JSON containing SQL statement and results from clinical_notes
        PATH_TO_ENGLISH = 'lang_store/english.csv'
        PATH_TO_DUMP = 'emr.sql'
        CMD_STR = 'python3 -m ln2sql.main -d ' + PATH_TO_DUMP + ' -l ' + PATH_TO_ENGLISH + ' -j out.json -i ' + '\"' + str(js['NLQuery']) + '\"'   
        sql_text = subprocess.run(CMD_STR, cwd='ln2sql/', shell=True, capture_output=True)
        query_str = str(sql_text.stdout.decode('utf-8'))
        query_str = query_str.replace("\n", " ").strip()
        
        to_return = {"Query": str(query_str)}
        return to_return
        
    
    def processText(self, free_text, pid):
        model = medacy_model_clinical_notes.load()
        attributes = {'P_ID':pid, 'Drug':'NULL', 'Strength':'NULL', 'Duration':'NULL', 'Route':'NULL', 'Form':'NULL', 'ADE':'NULL', 'Dosage':'NULL', 'Reason':'NULL', 'Frequency':'NULL', 'Note': free_text}
        for i in model.predict(free_text):
            attributes[i.tag] = i.text
        cnx = mysql.connector.connect(user='root', password='aksjhs',
                              host='localhost',
                              database='clinical')
        cur = cnx.cursor()
        add_data = ("INSERT INTO clinical_notes "
                    "(P_ID, LoggedDate, Drug, Strength, Duration, Route, Form, ADE, Dosage, Reason, Frequency, Note) "
                    "VALUES (%(P_ID)s, CURDATE(), %(Drug)s, %(Strength)s, %(Duration)s, %(Route)s, %(Form)s, %(ADE)s, %(Dosage)s, %(Reason)s, %(Frequency)s, %(Note)s)")
        cur.execute(add_data, attributes)
        return open("response.html").read().format(pid=attributes["P_ID"], 
                                                Drug=attributes["Drug"], 
                                                Strength=attributes["Strength"],
                                                Duration=attributes["Duration"],
                                                Route=attributes["Route"],
                                                Form=attributes["Form"],
                                                ADE=attributes["ADE"],
                                                Dosage=attributes["Dosage"],
                                                Reason=attributes["Reason"],
                                                Frequency=attributes["Frequency"])
        
        

#nlp = NLPUnit()
#nlp.processRequest(json.loads('{"Comments":"I prescribed Advil to Joun for his severe pain"}'))    
    
        
