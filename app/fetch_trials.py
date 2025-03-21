import requests
from datetime import datetime
from app.models import ClinicalTrial
from app import db

API_URL = "https://clinicaltrials.gov/api/v2/studies?query.cond=cancer&fields=OfficialTitle|BriefSummary|NCTId|LeadSponsor|Condition|StudyFirstSubmitDate&sort=StudyFirstSubmitDate&pageSize=20"

def fetch_and_store_trials(app):
    with app.app_context():
        response = requests.get(API_URL)
        data = response.json()

        studies = data.get("studies", [])

        for study in studies:
            try:
                trial_id = study["protocolSection"]["identificationModule"]["nctId"]
                title = study["protocolSection"]["identificationModule"].get("officialTitle", "No title provided")
                sponsor = study["protocolSection"]["sponsorCollaboratorsModule"]["leadSponsor"].get("name", "Unknown Sponsor")
                sponsor_class = study["protocolSection"]["sponsorCollaboratorsModule"]["leadSponsor"].get("class", "Unknown Class")
                summary = study["protocolSection"]["descriptionModule"].get("briefSummary", "No summary available")
                submit_date_str = study["protocolSection"]["statusModule"].get("studyFirstSubmitDate", None)

                if submit_date_str:
                    first_submit_date = datetime.strptime(submit_date_str, "%Y-%m-%d")
                else:
                    first_submit_date = None

                existing_trial = ClinicalTrial.query.get(trial_id)
                if existing_trial:
                    continue 

                new_trial = ClinicalTrial(
                    id=trial_id,
                    title=title,
                    sponsor_name=sponsor,
                    sponsor_class=sponsor_class,
                    summary=summary,
                    first_submit_date=first_submit_date
                )

                db.session.add(new_trial)

            except KeyError as e:
                print(f"Skipping a trial due to missing key: {e}")

        db.session.commit()
        print(f"{len(studies)} trials processed successfully!")