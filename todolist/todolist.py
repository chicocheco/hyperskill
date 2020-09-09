import sys
from datetime import datetime, timedelta, date

from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'  # correct would be a plural name
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=date.today())

    def __repr__(self):
        return self.task


class ToDoApp:
    menu = "\n1) Today's tasks\n" \
           "2) Week's tasks\n" \
           "3) All tasks\n" \
           "4) Missed tasks\n" \
           "5) Add task\n" \
           "6) Delete task\n" \
           "0) Exit"

    def __init__(self):
        self.create_database()
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
        self.start()

    @staticmethod
    def create_database():
        # if exists, it does nothing
        Base.metadata.create_all(engine)

    def start(self):
        while True:
            print(self.menu)
            choice = input()
            if choice == '1':
                self.print_todays_tasks()
            elif choice == '2':
                self.print_weeks_tasks()
            elif choice == '3':
                self.print_all_tasks()
            elif choice == '4':
                self.print_missed_tasks()
            elif choice == '5':
                self.add_task()
            elif choice == '6':
                self.delete_task()
            else:
                print('Bye!')
                sys.exit()

    def print_todays_tasks(self):
        rows = self.session.query(Task).filter(Task.deadline == date.today()).all()
        print(f"Today {datetime.strftime(datetime.today(), '%d %b')}:")
        if rows:
            for i, task in enumerate(rows, start=1):
                print(f'{i}. {task}')
        else:
            print('Nothing to do!')

    def print_weeks_tasks(self):
        curr_date = datetime.today()
        for day in range(7):
            rows = self.session.query(Task).filter(Task.deadline == curr_date.date()).all()
            print(f"\n{datetime.strftime(curr_date, '%A %d %b')}")
            if rows:
                for i, task in enumerate(rows, start=1):
                    print(f'{i}. {task}')
            else:
                print('Nothing to do!')
            curr_date += timedelta(days=1)

    def print_all_tasks(self):
        rows = self.session.query(Task).order_by(Task.deadline).all()
        print('All tasks:')
        if rows:
            for i, task in enumerate(rows, start=1):
                date_frt = datetime.strftime(task.deadline, '%e %b').strip()
                print(f"{i}. {task}. {date_frt}")
        else:
            print('Nothing to do!')

    def print_missed_tasks(self):
        rows = self.session.query(Task).filter(Task.deadline < date.today()).all()
        print('Missed tasks:')
        if rows:
            for i, task in enumerate(rows, start=1):
                date_frt = datetime.strftime(task.deadline, '%e %b').strip()
                print(f"{i}. {task}. {date_frt}")
        else:
            print('Nothing is missed!')

    def add_task(self):
        text_task = input('Enter task\n')
        deadline_task = input('Enter deadline\n')
        new_row = Task(task=text_task,
                       deadline=datetime.strptime(deadline_task, '%Y-%m-%d').date()
                       )
        self.session.add(new_row)
        self.session.commit()
        print('The task has been added!')

    def delete_task(self):
        print('Choose the number of the task you want to delete:\n')
        rows = self.session.query(Task).order_by(Task.deadline).all()
        if rows:
            for i, task in enumerate(rows, start=1):
                date_frt = datetime.strftime(task.deadline, '%e %b').strip()
                print(f"{i}. {task}. {date_frt}")
        to_delete = int(input())
        row_to_delete = rows[to_delete - 1]
        if row_to_delete:
            self.session.delete(row_to_delete)
            self.session.commit()
            print('The task has been deleted!')
        else:
            print('Nothing to delete')


if __name__ == '__main__':
    app = ToDoApp()
