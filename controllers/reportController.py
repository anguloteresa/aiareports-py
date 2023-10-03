from models.report import Report
from extensions import db
from flask import Flask, request, jsonify
from flask_restful import marshal_with, fields
from sqlalchemy.sql import func


ReportModel = {
  "id": fields.Integer,
  "title": fields.String,
  "owner": fields.String,
  "date": fields.DateTime,
  "body": fields.String,
}


@marshal_with(ReportModel)
def getReportsAll():
  reports = Report.query.all()
  return reports

@marshal_with(ReportModel)
def getReportGroup(user_id):
  reports = Report.query.filter_by(owner = user_id).all()
  return reports

@marshal_with(ReportModel)
def getUserReport(user_id, report_id):
  report = Report.query.filter_by(owner = user_id).filter_by(id = report_id).all()
  return report


@marshal_with(ReportModel)
def createReport():
  if request.method == 'POST':
    data = request.json
    print(data)
    title = data["title"]
    owner = data["owner"]
    report = Report(title=title, owner=owner)
    
    db.session.add(report)
    db.session.commit()
    
    return report
  
  return {"message": "Método no permitido"}, 405  # Ejemplo: Devuelve un mensaje de error y un código 405 para otros métodos HTTP

@marshal_with(ReportModel)
def deleteReport(user_id, report_id):
  # Retrieve report from db
  report = Report.query.filter_by(owner = user_id).filter_by(id = report_id).first()
  
  db.session.delete(report)
  db.session.commit()
  
  return {"message:" : "Reporte eliminado"}

@marshal_with(ReportModel)
def editReport(user_id, report_id):
  report = Report.query.filter_by(owner = user_id).filter_by(id = report_id).first()

  report = report.query.get_or_404(report_id)
  
  if request.method == 'POST':
    data = request.json
    title = data["title"]
    owner = data["owner"]
    body = data["body"] or ""
    
    report.title = title
    report.owner = owner
    report.date = func.now()
    
    db.session.add(report)
    db.session.commit()

    return report
  
  return {"message": "Método no permitido"}, 405  # Ejemplo: Devuelve un mensaje de error y un código 405 para otros métodos HTTP

