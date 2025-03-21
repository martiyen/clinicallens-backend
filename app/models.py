from . import db

class ClinicalTrial(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    sponsor_name = db.Column(db.String, nullable=False)
    sponsor_class = db.Column(db.String, nullable=False)
    summary = db.Column(db.String, nullable=False)
    first_submit_date = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "sponsor_name": self.sponsor_name,
            "sponsor_class": self.sponsor_class,
            "summary": self.summary,
            "fist_submit_date": self.first_submit_date,
        }