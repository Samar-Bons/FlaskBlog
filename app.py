import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

#Function to connect to db and return conn object
def get_db_connection():
    conn = sqlite3.connect('database.db')

    #Making every row behave as a dictionary
    conn.row_factory = sqlite3.Row 
    return conn

#Function to fetch a post using given post_id.
#returns a row as a dictionary object
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',(post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


#Creating Flask instance and a simple secret_key
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mySecretKey'

#Default view function
@app.route('/')

def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

#View function for specific posts using post_id
@app.route('/<int:post_id>')

def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

#View function for creating a new post
@app.route('/create', methods=('GET','POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            #Reloads the create page with a flash warning
            flash('Title is needed!')
        else:
            #insert new post in sql db
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title,content) VALUES (?,?)',
                (title,content))
            
            conn.commit()
            conn.close()
            #redirect to homepage
            return redirect(url_for('index'))

    return render_template('create.html')
  

#View function to edit an existing post
@app.route('/<int:id>/edit', methods=('GET','POST'))
def edit(id):
	post = get_post(id)
	
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']
		
		if not title:
            #reload edit page with a flash warning
			flash('Title is required!')
		else:
            #update sql db
			conn = get_db_connection()
			conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',(title,content,id))
			conn.commit()
			conn.close()
            #redirect to homepage
			return redirect(url_for('index'))
			
						
	return render_template('edit.html', post=post)
	
#View function to delete an existing post
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    #Retrieve post to display a flash message later with Post title
	post = get_post(id)
	conn = get_db_connection()
    
    #delete row from sql db
	conn.execute('DELETE FROM posts WHERE id=?',(id,))
	conn.commit()
	conn.close()
    #Flash message with title retrived earlier
	flash('"{}" was successfully deleted!'.format(post['title']))
	#return to homepage
    return redirect(url_for('index'))


