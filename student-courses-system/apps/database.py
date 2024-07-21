from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()