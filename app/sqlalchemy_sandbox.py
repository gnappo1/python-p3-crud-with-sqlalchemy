#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, select, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enroll_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:', echo=True, future=True)
    Base.metadata.create_all(engine)
    # Session = sessionmaker(bind=engine)
    session = Session(engine)

    #Instantiation
    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    #Save and BulkSave
    # session.add(albert_einstein)
    # session.add_all([albert_einstein, alan_turing])
    session.bulk_save_objects([albert_einstein, alan_turing])
    # Unfortunately, bulk_save_objects() does not associate the records with the session, so we don't update our records' IDs. Take this into consideration when creating records in your own code

    session.commit()
    # print(f"New student ID is {albert_einstein.id}.")
    # print(f"New student ID is {alan_turing.id}.")

    #Order
    # students = session.query(Student).order_by(Student.name).all()
    # oldest_student = session.query(Student).order_by(desc(Student.birthday)).limit(1)[0]

    #Filter
    # smart_alberts = session.query(Student.name).filter(Student.name.like('%Albert%'), Student.grade > 5)


    #Update
    # for student in session.query(Student):
    #     student.grade += 1
    # session.commit()
    # session.query(Student).update({
    #     Student.grade: Student.grade + 1
    # })
    # session.query(Student).update({
    #     Student.grade: Student.grade + 1
    # })
    # student_count = session.query(func.count(Student.id)).first()
    # student_sum_grade = session.query(func.sum(Student.grade)).first()
    # print([student for student in students])
    # print(student_count[0], student_sum_grade[0])
    # print(f"Class avg grade: {student_sum_grade[0] / student_count[0]}")
    # print([rec.name for rec in smart_alberts])

    #DELETE
    # filtered_einstein = session.query(Student).filter(Student.name == "Albert Einstein")
    filtered_einstein = select(Student).where(Student.name == "Albert Einstein")
    # einstein = filtered_einstein.first()
    for person in session.scalars(filtered_einstein):
        print(person)

    print(session.get(Student, 1))
    # session.delete(einstein)
    # session.commit()
    # einstein = filtered_einstein.first()
    # print(einstein)

    #or
    # filtered_einstein = session.query(Student).filter(Student.name == "Albert Einstein")
    # filtered_einstein.delete()
    # einstein = filtered_einstein.first()
    # print(einstein)
    # import ipdb; ipdb.set_trace()
