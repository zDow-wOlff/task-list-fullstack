from app import db

class Task(db.Model):
    __tablename__ = 'task'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    entityName = db.Column(db.String(255))
    taskType = db.Column(db.String(255))
    date = db.Column(db.String(255))
    time = db.Column(db.String(255))
    contactPerson = db.Column(db.String(255))
    status = db.Column(db.String(255))
    note = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'entityName': self.entityName,
            'taskType': self.taskType,
            'date': self.date,
            'time': self.time,
            'contactPerson': self.contactPerson,
            'status': self.status,
            'note': self.note,
            'done': self.done
        }
