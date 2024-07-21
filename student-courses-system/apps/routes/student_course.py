from apps.database import db
from apps.models import Student
from flask import Blueprint, request, jsonify, abort


scBP = Blueprint('stdent_courses', __name__, "/student_courses/")