from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:TheBlog@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO']=True

db = SQLAlchemy(app)
app.secret_key = '71121'

#class to keep usernames
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    usrnm = db.Column(db.String(20))
    psswrd = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref = 'owner')

    def __init__ (self, usrnm, psswrd):
        self.usrnm = usrnm
        self.psswrd = psswrd



#class to keep n validate blog entries
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1000))
    created = db.Column(db.DateTime)
    owner_id=db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.owner = owner
        self.created = datetime.utcnow()



    def is_valid(self):
        if self.title and self.body and self.created:
            return True
        else:
            return False

#Global validation functions
def empty_field(fields):
    if len(fields) > 0:
        return True
    else:
        return False

def validate_field(fields):
    if " " not in fields:
        if len(fields) > 2 and len(fields) < 21:
            return True
        else:
            return False

def match(p_one, p_two):
    if p_one == p_two:
        return True
    else:
        return False



#requires login or create username
# add other routes allowed per assignment description
@app.before_request
def require_login():
    allowed_routes = ['signup', 'login', 'display_blog_entries', 'index']
    if request.endpoint not in allowed_routes and 'usrnm' not in session:
        return redirect('/login')


#root route with index handler goes to index.html template displaying all users
@app.route("/")
def index():
    all_users = User.query.filter_by(usrnm).all()
    return render_template('index.html', title = "Home", all_users = all_users)

# login route
@app.route('/login', methods = ['POST', 'GET'])
def login():
    #error variables with counter
    usrnm_error = ''
    psswrd_error = ''
    error_count = 0

    if request.method == 'POST':
        usrnm = request.form['usrnm']
        psswrd = request.form['psswrd']
        #original location of ...... user = User.query.filter_by(usrnm=usrnm).first()  moved to below validation conditionals

        #validate field entries
        if not empty_field(usrnm):
            usrnm_error = "Enter a valid username."
            error_count = error_count + 1

        if not empty_field(psswrd):
            psswrd_error = "Enter a valid password."
            error_count = error_count + 1

        if not validate_field(usrnm):
            usrnm_error = "Username must be 3-20 characters with no spaces."
            error_count = error_count + 1

        if not validate_field(psswrd):
            psswrd_error = "Password must be 3-20 characters with no spaces."
            error_count = error_count + 1

        if error_count > 0 :
            return render_template('login.html', usrnm=usrnm, psswrd='', verify='', usrnm_error=usrnm_error, psswrd_error=psswrd_error, vpsswrd_error=vpsswrd_error)

        user = User.query.filter_by(usrnm=usrnm).first()

        if user and user.psswrd == psswrd:
            session['usrnm'] = usrnm
            flash("Logged in")
        else:
            flash("Password incorrect, or user does not exist", "Error")

    return render_template('login.html')



#Sign up route
@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    #error variables with counter
    usrnm_error = ''
    psswrd_error = ''
    vpsswrd_error = ''
    error_count = 0

    if request.method == 'POST':
        usrnm = request.form['usrnm']
        psswrd = request.form['psswrd']
        verify = request.form['verify']

        #validate field entries
        if not empty_field(usrnm):
            usrnm_error = "Enter a valid username."
            error_count = error_count + 1

        if not empty_field(psswrd):
            psswrd_error = "Enter a valid password."
            error_count = error_count + 1

        if not empty_field(verify):
            vpsswrd_error = "Password must be verified."
            error_count = error_count + 1

        if not validate_field(usrnm):
            usrnm_error = "Username must be 3-20 characters with no spaces."
            error_count = error_count + 1

        if not validate_field(psswrd):
            psswrd_error = "Password must be 3-20 characters with no spaces."
            error_count = error_count + 1

        if not match(psswrd, verify):
            vpsswrd_error = "Passwords must match."
            error_count = error_count + 1

        if error_count > 0 :
            return render_template('signup.html', usrnm=usrnm, psswrd='', verify='', usrnm_error=usrnm_error, psswrd_error=psswrd_error, vpsswrd_error=vpsswrd_error)

        existing_user = User.query.filter_by(usrnm=usrnm).first()
        if not existing_user:
            new_user = User(usrnm, psswrd)
            db.session.add(new_user)
            db.session.commit()
            session['usrnm'] = usrnm
            return redirect('/login')
        else:
            return ",h1>This username already exists</h1>"
    return render_template('signup.html')








@app.route("/blog")
def display_blog_entries():
    entry_id = request.args.get('id')
    user = request.args.get()
    if (entry_id):
        entry = Blog.query.get(entry_id)
        return render_template('single_entry.html', title = "Blog Entry", entry = entry)

    if (user):
        blogs = User.query.filter_by(blogs = blogs).all()

    #list all entries

    else:
        all_entries = Blog.query.all()

    return render_template('all_entries.html', title = "All Entries", all_entries = all_entries)




@app.route("/new_entry", methods = ['GET', 'POST'])
def new_entry():
    #display form and create new blog post
    if request.method == 'POST':
        new_entry_title = request.form['title']
        new_entry_body = request.form['body']
        user = User.query.filter_by(usrnm=session['usrnm']).first()
        new_entry = Blog(new_entry_title, new_entry_body, user)

        if new_entry.is_valid():
            db.session.add(new_entry)
            db.session.commit()

# new post displayed
            url = "/blog?id="+str(new_entry.id)
            return redirect(url)

        else:
            flash("A blog title and body are required to have a valid entry.")
            return render_template('new_entry_form.html', title = "Create new blog entry",
                    new_entry_title = new_entry_title, new_entry_body = new_entry_body)

    else:
         #this else is for GET request
         return render_template('new_entry_form.html', title = "Create new blog entry")



#logs user out and deletes session
@app.route('/logout')
def logout():
    del session['usrnm']
    return redirect('/')




if __name__ == '__main__':
    app.run()












































if __name__ == '__main__':
    app.run()
