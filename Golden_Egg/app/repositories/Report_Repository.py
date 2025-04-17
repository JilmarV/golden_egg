from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.Report import Report
from app.schemas.Report_Schema import ReportCreate, ReportUpdate

class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_report(self, report_id: int) -> Optional[Report]:
        return self.db.query(Report).filter(Report.id == report_id).first()

    def get_reports_by_type(self, report_type: str) -> List[Report]:
        return self.db.query(Report).filter(Report.type == report_type).all()

    def get_reports(self, skip: int = 0, limit: int = 100) -> List[Report]:
        return self.db.query(Report).offset(skip).limit(limit).all()

    def create_report(self, report: ReportCreate) -> Report:
        db_report = Report(**report.model_dump())
        self.db.add(db_report)
        self.db.commit()
        self.db.refresh(db_report)
        return db_report

    def update_report(self, report_id: int, report: ReportUpdate) -> Optional[Report]:
        db_report = self.get_report(report_id)
        if db_report:
            update_data = report.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_report, field, value)
            self.db.commit()
            self.db.refresh(db_report)
        return db_report

    def delete_report(self, report_id: int) -> bool:
        db_report = self.get_report(report_id)
        if db_report:
            self.db.delete(db_report)
            self.db.commit()
            return True
        return False