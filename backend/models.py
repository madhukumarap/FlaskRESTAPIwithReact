from exts import db

#     """
# class Recipe:
#     id:int primary key
#     title:str
#     description:str (text)        
# """
class Recipe(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    
    def __repr__(self):  #the repr works as a string representation of the object
        return f'<Recipe {self.title}>' 
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self,title,description):
        self.title = title
        self.description = description
        db.session.commit()
        