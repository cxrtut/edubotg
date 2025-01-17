from flask import Flask, render_template, redirect, url_for, request, session
from flask import Flask
from edubotApp import db, create_app
from edubotApp.models import User


import os

app = create_app()


app.secret_key = os.urandom(24)




# Dummy user data (for simplicity, this will be a dictionary)
#users = {}

# Configure database

# Index route
@app.route('/')
def index():
    return render_template('index.html')

# Home route (protected area)
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Fetch the user from the database using the session's username
    user = User.query.filter_by(username=session['username']).first()
    
    if not user:
        return "User not found", 404

    return render_template('home.html', user=user)


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = user.username
            return redirect(url_for('home'))
        else:
            return 'Invalid credentials. Please try again.'
    return render_template('login.html')

# Signup route
# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if not User.query.filter_by(username=username).first():
            new_user = User(username=username, password=password, email=email)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return 'User already exists. Please log in.'
    return render_template('signup.html')



# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove 'username' from session
    return redirect(url_for('index'))






@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Fetch the user from the database using the session's username
    user = User.query.filter_by(username=session['username']).first()

    if not user:
        return "User not found", 404

    if request.method == 'POST':
        # Get the updated username and email from the form
        new_username = request.form['username']
        new_email = request.form['email']
        
        # Update the user's information
        user.username = new_username
        user.email = new_email
        
        # Commit the changes to the database
        db.session.commit()

        # Optionally, you can update the session to reflect the new username
        session['username'] = new_username

        return redirect(url_for('home'))  # Redirect to refresh the profile page with updated data

    return render_template('profile.html', user=user)



if __name__ == '__main__':
    app.run(debug=True)

