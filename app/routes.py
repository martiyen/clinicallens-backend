from flask import Blueprint, jsonify
from app import db
from app.models import ClinicalTrial
from sqlalchemy.sql import func, select
from collections import Counter

trials = Blueprint("trials", __name__)

@trials.route("/trials", methods=["GET"])
def get_trials():
    trials = ClinicalTrial.query.all()
    return jsonify([trial.to_dict() for trial in trials])

@trials.route("/trials/count", methods=["GET"])
def get_trial_count():
    count = db.session.query(func.count(ClinicalTrial.id)).scalar()
    return jsonify({"total_trials": count})

@trials.route("/trials/latests", methods=["GET"])
def get_latest_trials():
    trials = ClinicalTrial.query.order_by(ClinicalTrial.first_submit_date.desc()).limit(10).all()
    return jsonify([trial.to_dict() for trial in trials])

@trials.route("/trials/best-sponsors", methods=['GET'])
def get_best_sponsor():
    sponsors = db.session.execute(select(ClinicalTrial.sponsor_name)).all()
    sponsor_list = [sponsor[0] for sponsor in sponsors]
    sponsor_counts = Counter(sponsor_list)
    most_common = sponsor_counts.most_common(3)
    most_common_json = [{"sponsorName":name, "count": count} for name, count in most_common]
    return most_common_json

@trials.route("/trials/<query>", methods=['GET'])
def get_by_keyword(query):
    trials = ClinicalTrial.query.filter(func.lower(ClinicalTrial.summary).contains(func.lower(query))).all()
    return jsonify([trial.to_dict() for trial in trials])

@trials.route("/trials/random", methods=['GET'])
def get_random_trial():
    trials = [ClinicalTrial.query.order_by(func.random()).first()]
    return jsonify([trial.to_dict() for trial in trials])