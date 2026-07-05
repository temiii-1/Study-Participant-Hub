import requests
import json

# Query ClinicalTrials.gov API for actively recruiting UT Austin studies
url = "https://clinicaltrials.gov/api/v2/studies"
params = {
    "query.term": "University of Texas Austin",
    "filter.overallStatus": "RECRUITING",
    "pageSize": 200,
}

response = requests.get(url, params=params)
print("Status code:", response.status_code)
print("Response preview:", response.text[:200])
data = response.json()

studies = []

for study in data.get("studies", []):
    protocol = study.get("protocolSection", {})

    raw_date = protocol.get("statusModule", {}).get("studyFirstSubmitDate", "")
    if raw_date:
        parts = raw_date.split("-")
        date = f"{parts[1]}/{parts[2]}/{parts[0]}"
    else:
        date = ""

    # get category from conditions
    conditions = protocol.get("conditionsModule", {}).get("conditions", [])
    category = conditions[0] if conditions else "Other"
    
    title = protocol.get("identificationModule", {}).get("briefTitle", "")
    description = protocol.get("descriptionModule", {}).get("briefSummary", "")
    eligibility = protocol.get("eligibilityModule", {}).get("eligibilityCriteria", "")
    min_age = protocol.get("eligibilityModule", {}).get("minimumAge", "")
    max_age = protocol.get("eligibilityModule", {}).get("maximumAge", "")
    nct_id = protocol.get("identificationModule", {}).get("nctId", "")

    contacts = protocol.get("contactsLocationsModule", {}).get("centralContacts", [])
    contact = ""
    if contacts:
        contact = f"{contacts[0].get('name', '')} {contacts[0].get('email', '')}"


    if "utexas.edu" not in contact.lower():
        continue

    studies.append({
        "title": title,
        "date": date,
        "description": description,
        "eligibility": [eligibility],
        "compensation": "",
        "contact": contact,
        "category": category,
        "source": f"https://clinicaltrials.gov/study/{nct_id}",
        "min_age": min_age,
        "max_age": max_age
    })

print(f"Found {len(studies)} recruiting UT Austin studies")
for study in studies[:5]:
    print(f"TITLE: {study['title'][:60]}")
    print(f"CONTACT: {study['contact']}")
    print(f"DATE: {study['date']}")
    print(f"CATEGORY: {study['category']}")
    print("---")

with open("clinicaltrials.json", "w") as f:
    json.dump(studies, f, indent=2)

print("Saved to clinicaltrials.json")