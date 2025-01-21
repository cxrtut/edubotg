from website import create_app
from flask import Flask, render_template, redirect, url_for, session
app = create_app()


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('views.home'))

@app.route('/')
def home():
    return render_template('index.html', username=session.get('username'))

@app.route('/settings')
def settings():
    if 'username' in session:
        return render_template('settings.html', username=session['username'])
    return redirect(url_for('views.home'))

if __name__ == '__main__':
    app.run(debug=True)

