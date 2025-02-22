from flask import request, jsonify
from .postify import app, db
from .models import User


@app.route('/users', methods=['POST'])
