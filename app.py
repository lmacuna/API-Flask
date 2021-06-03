from flask import Flask, request, jsonify
from flask import render_template,redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/flaskcontacts'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#settings
app.secret_key = 'mysecretkey'

class Contact(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    fullname = db.Column(db.String(100),unique=True)
    phone = db.Column(db.Integer,unique=True)
    email = db.Column(db.String(20),unique=True)

    def __init__(self,fullname,phone,email):
        self.fullname = fullname
        self.phone = phone
        self.email = email
db.create_all()
class ContactSchema(ma.Schema):
    class Meta:
        fields = ('id','fullname','phone','email')
contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)  

@app.route('/add_contact', methods=['POST'])
def add_contact():
    fullname = request.form['fullname']
    phone = request.form['phone']
    email = request.form['email']
    new_contact = Contact(fullname,phone,email)
    db.session.add(new_contact)
    db.session.commit()
    print(new_contact)
    flash('Contact Added Successfully')
    
    return redirect(url_for('index'))
    
    #return 'add contact' 

@app.route('/contacts',methods=['GET'])
def get_contacts():
    all_contacts = Contact.query.all() 
    result = contacts_schema.dump(all_contacts)
    return jsonify(result)

@app.route('/')
def index():
    all_contacts = Contact.query.order_by(Contact.id).all()
    result = contacts_schema.dump(all_contacts)
   
    
    return render_template('index.html', Contacts = result )
 
 
    
#URL en proceso
    
 
    
@app.route('/')
def inicial():

    return render_template('index.html')



@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit_contact(id):
    edit_contact = Contact.query.get(id)
   
    db.session.commit()
    contact = contacts_schema.dump(id)
    print(edit_contact)
    flash("EDIT SUCCESSFULLY")
    return render_template('edit.html',contact = edit_contact)


@app.route('/update_contact/<id>',methods=['POST','GET'])
def update_contact(id):
    contact = Contact.query.get(request.form.get('id'))
    fullname = request.form['fullname']
    phone = request.form['phone']
    email = request.form['email']
    
    contact.fullname = fullname
    contact.phone = phone
    contact.email = email
    contact = Contact(fullname,phone,email)
    db.session.bulk(contact)
    db.session.commit()
    flash("Update Successfully")
    return redirect(url_for('index'))    


@app.route('/delete/<id>/',methods=['GET','POST'])
def delete_contact(id):
    delete_contact = Contact.query.get(id)
    if delete_contact:

       db.session.delete(delete_contact)
       db.session.commit()
       
       print(delete_contact)
    flash("Delete Successfully")   
    return redirect(url_for('index'))            


@app.errorhandler(404)
def page_not_found(error):
	return render_template("error.html",error="Página no encontrada..."), 404




if __name__ == '__main__':
    app.run(debug=True,port=3000) 