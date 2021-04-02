from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta, date
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.__tablename__


if __name__ == "__main__":
    engine = create_engine('sqlite:///todo.db?check_same_thread=False')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    choice = 999999
    while choice:
        print()
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")
        choice = int(input(">"))

        if choice == 1:
            today = datetime.today()
            rows = session.query(Table).filter(Table.deadline == today.date()).all()
            print()
            print('Today ' + str(today.day) + ' ' + str(today.strftime('%b')) + ':')
            if rows:
                pos = 1
                for row in rows:
                    print(str(pos) + '. ' + row.task + '.')
                    pos += 1
            else:
                print("Nothing to do!")
        elif choice == 2:
            count = 0
            today = datetime.today()
            weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                        'Friday', 'Saturday', 'Sunday']

            while count <= 7:
                day = today + timedelta(days=count)
                rows = session.query(Table).filter(Table.deadline == day.date()).all()
                print()
                print(weekdays[day.weekday()] + ' ' + str(day.day) + ' ' + str(day.strftime('%b')) + ':')
                if rows:
                    pos = 1
                    for row in rows:
                        print(str(pos) + '. ' + row.task + '. ' + str(row.deadline.day) + ' ' + str(row.deadline.strftime('%b')))
                        pos += 1
                else:
                    print("Nothing to do!")
                count += 1
        elif choice == 3:
            rows = session.query(Table).order_by(Table.deadline).all()
            print()
            print("All tasks:")
            if rows:
                pos = 1
                for row in rows:
                    print(str(pos) + '. ' + row.task + '. ' + str(row.deadline.day) + ' ' + str(row.deadline.strftime('%b')))
                    pos += 1
            else:
                print("No task added!")
        elif choice == 4:
            print()
            print("Missed tasks:")
            today = datetime.today()
            rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
            if rows:
                pos = 1
                for row in rows:
                    print(str(pos) + '. ' + row.task + '. ' + str(row.deadline.day) + ' ' + str(row.deadline.strftime('%b')))
                    pos += 1
            else:
                print("Nothing is missed!")
        elif choice == 5:
            print()
            print("Enter task")
            task = input(">")
            print("Enter deadline")
            year, month, day = input(">").split('-')
            deadline = date(int(year), int(month), int(day))
            row = Table(task=task, deadline=deadline)
            session.add(row)
            session.commit()
            print("The task has been added!")
        elif choice == 6:
            print()
            print("Choose the number of the task you want to delete:")
            rows = session.query(Table).order_by(Table.deadline).all()
            if rows:
                pos = 1
                for row in rows:
                    print(str(pos) + '. ' + row.task + '. ' + str(row.deadline.day) + ' ' + str(row.deadline.strftime('%b')))
                    pos += 1
                number = int(input(">"))
                session.delete(rows[number - 1])
                session.commit()
                print("The task has been deleted!")
            else:
                print("Nothing to delete!")
    print()
    print("Bye!")
