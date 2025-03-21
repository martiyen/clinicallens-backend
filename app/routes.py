from flask import Blueprint, jsonify
from app import db
from app.models import ClinicalTrial
from sqlalchemy.sql import func
from app.fetch_trials import fetch_and_store_trials

main = Blueprint("main", __name__)

@main.route("/trials", methods=["GET"])
def get_trials():
    trials = ClinicalTrial.query.all()
    return jsonify([trial.to_dict() for trial in trials])

@main.route("/trials/count", methods=["GET"])
def get_trial_count():
    count = db.session.query(func.count(ClinicalTrial.id)).scalar()
    return jsonify({"total_trials": count})

@main.route("/trials/latest", methods=["GET"])
def get_latest_trials():
    trials = ClinicalTrial.query.order_by(ClinicalTrial.first_submit_date.desc()).limit(10).all()
    return jsonify([trial.to_dict() for trial in trials])

@main.route("/trials/update", methods = ["POST"])
def update_trials():
    fetch_and_store_trials()
    return "Trials updated"

@main.route("/trials/delete/all", methods = ["DELETE"])
def delete_all():
    db.drop_all()
    db.create_all()
    return "Trials deleted"