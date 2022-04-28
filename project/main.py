from flask import Blueprint, render_template, session, Flask
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import User, Chats, Messages
from . import db

app = Flask(__name__)

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/search')
@login_required
def search():
    return render_template('search.html')

@main.route('/search', methods=['POST'])
@login_required
def search_post():
    name = request.form.get('search')
    user = User.query.filter_by(name=name).first()
    if user:
        session['chatuser'] = user.id
        return render_template('chat.html', user=user, current_user=current_user)
    else:
        return render_template('test.html', user=user, current_user=current_user)



@main.route('/send', methods=['POST'])
@login_required
def send_post():
    message = request.form.get('message')
    userid = session.get('chatuser')
    user1 = User.query.filter_by(id=userid).first()
    user2 = User.query.filter_by(id=current_user.id).first()
    if userid:
        chat = Chats.query.filter_by(user1=user1.id).filter_by(user2=user2.id).first()
        if not chat:
            chat = Chats.query.filter_by(user2=user1.id).filter_by(user1=user2.id).first()
        if not chat:
            new_chat = Chats(user1=user1.id, user2=user2.id)
            db.session.add(new_chat)
            db.session.commit()
            chat = new_chat

        new_message = Messages(author=user2.id, message=message, chat=chat.id)
        db.session.add(new_message)
        db.session.commit()

        messages = db.session.query(Messages, User).join(User, User.id==Messages.author).filter(Messages.chat == chat.id)
        m = [dict(i) for i in messages]
    else:
        messages = []

    return render_template('chat.html', user=user1, current_user=user2, messages=messages, str=str)