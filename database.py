import sqlite3 #python built in library for working with databases
import json #just reads our json file

#BUILD DATABASE: 1 database file, multiple tables/ spreadsheets inside it (studies,users,profiles)

# connect to database (creates the file if it doesn't exist)
conn = sqlite3.connect("studies.db")
cursor = conn.cursor() #conn is the connextion to the database and cursur is the toll used to actually run commands on it

#create user table for personal accounts
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")

#create profile tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        age TEXT,
        major TEXT,
        interests TEXT,
        medical_conditions TEXT,
        availability TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
""")

conn.commit()


cursor.execute("DELETE FROM studies")  # clear existing studies, re-insert with categories

# load Healthy Horns studies from JSON file
with open("studies.json", "r") as f:
    healthy_horns_studies = json.load(f)

# load ClinicalTrials studies
with open("clinicaltrials.json", "r") as f:
    clinicaltrials_studies = json.load(f)

all_studies = healthy_horns_studies + clinicaltrials_studies


# insert each study(as a row) into the database
for study in all_studies:
    cursor.execute("""
        INSERT INTO studies (title, date, description, eligibility, compensation, contact, category)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        study["title"],
        study["date"],
        study["description"],
        json.dumps(study["eligibility"]),
        study["compensation"],
        study["contact"],
        study["category"]
    ))

conn.commit()
conn.close()

print(f"Loaded {len(all_studies)} total studies into database")
print(f"Loaded {len(healthy_horns_studies)} Healthy Horns studies into database")
print(f"Loaded {len(clinicaltrials_studies)} ClinicalTrials studies into database")