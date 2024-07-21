from apps.database import db
from apps.models import Student
from flask import Blueprint, request, jsonify, abort

courseBP = Blueprint('courses', __name__, '/courses/')