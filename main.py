from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:flashblog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO']=True

db = SQLAlchemy(app)
app.secret_key = '071117'

#class to keep n validate blog entries
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1000))
    created = db.Column(db.Datetime)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.created = datetime.utcnow()

    def is_valid(self):
        if self.title and self.body and self.posted:
            return True
        else:
            return False


# index route for base URL
@app.route("/")
def index():
    return redirect("/blog")


@app.route("/blog")
def blog_posts():
    entry.id = request.args.get('id')
    if (entry_id):
        entry = Entry.query.get(entry_id)
        return render_template('single_entry.html', title = "Blog Entry", entry = entry)

    #list all entries
    sort = request.args.get('sort')
    if (sort == "newest"):
        all_entries = Entry.query.order_by(Entry.created.desc()).all()
    else:
        all_entries = Entry.query.all()
    return render_template('all_entries.html', title = "All Entries", all_entries = all_entries)

@app.route("/new_entry", methods = ['GET', 'POST'])
def new_entry():
    #display form and create new blog post
    if request.method == 'POST':
        new_entry_title = request.form['title']
        new_entry_body = request.form['body']
        new_entry = Entry(new_entry_title, new_entry_body)

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


if __name__ == '__main__':
    app.run()












































if __name__ == '__main__':
    app.run()
