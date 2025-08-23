from flask import Blueprint, render_template, request, jsonify
from .summarization.text_rank import textrank_summarize

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    return render_template("home.html")

# endpoint JSON (utile per fetch() dal frontend)
@main_bp.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json() or {}
    text = (data.get("text") or "").strip()
    
    return jsonify({"summary": textrank_summarize(text, top_n=3)})


