class user(db.model):
    id=db.Column('Uses_id',db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    password=db.Column(db.String(100))
    true=db.Column(db.String(100))
    def __init__(self,name,email,password):
        self.name=name
        self.email=email
        self.password=password
        self.true=False
    def get_name(self):
        return self.name
    def set_name(self,name):
        self.name=name
    def get_email(self):
        return self.email
    def set_email(self,email):
        self.email=email
    def set_password(self,password):
        self.password=password
    def get_true(self):
        return self.true
    def validate_true(self):
        self.true=True
class users(db.Model):
    id = db.Column('schools_id', db.Integer, primary_key = True)
    category=db.Column(db.String(100))
    name=db.Column(db.String(100))
    zone=db.Column(db.String(50))
    addr=db.Column(db.String(200))
    faculty = db.Column(db.String(300))
    PSLE=db.Column(db.Integer)
    L1R5=db.Column(db.Integer)
    L1R4=db.Column(db.Integer)
    def __init__(self,category,name,zone,addr):
        self.name=name
        self.zone=zone
        self.addr=addr
        self.category=category
    def set_PSLE(self,psle):
        self.PSLE=psle
    def set_L1R5(self,l1r5):
        self.L1R5=l1r5
    def set_L1R4(self,l1r4):
        self.L1R4=l1r4
    def set_faculty(self,faculty):
        self.faculty=faculty