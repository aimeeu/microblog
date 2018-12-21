import logging
from application import app, db, errors, email
from application.forms import (
    LoginForm, RegistrationForm, EditProfileForm, PostForm,
    ResetPasswordRequestForm, ResetPasswordForm
)
from application.models import User, Post
from flask import (
    render_template, flash, redirect, url_for, request
)
from flask_login import (
    current_user, login_user, logout_user, login_required
)
from werkzeug.urls import url_parse
from datetime import datetime

logger = logging.getLogger(__name__)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    '''
    show blog posts written by all
the people that are followed by the logged in user
    :return:
    '''
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    # posts = current_user.followed_posts().all()
    # The return value from paginate is a Pagination object. The items
    # attribute of this object contains the list of items in the requested page
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, app.config[
        'POSTS_PER_PAGE'], False)
    next_url = url_for('index',
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index',
                       page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,
                                                                app.config[
                                                                    'POSTS_PER_PAGE'],
                                                                False)
    next_url = url_for('explore',
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore',
                       page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user();
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    '''
    Try to load the user from the database using a query by the username.
    Call first_or_404(), which works exactly like first() when  there are
    results, but when there are no results, automatically sends a 404
    error back to the client. Executing the query in this way saves having to
    check if the query returned a user, because when the username does not
    exist in the database the function will not return and instead a
    404 exception will be raised. If the database query does not trigger a
    404 error, then that means that a user was found.
    Initialize a fake list of posts for this user.
    Render a new user.html template, passing the user and the list of posts.
    :param username:
    :return: user.html
    '''

    this_user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(user_id=this_user.id).paginate(page,
                                                                app.config[
                                                                    'POSTS_PER_PAGE'],
                                                                False)
    next_url = url_for('user', username=username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user', username=username,
                       page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user=this_user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    '''
    If validate_on_submit()
    returns True I copy the data from the form into the user object and then
    write the object to the
    database. But when validate_on_submit() returns False it can be due to two
    different
    reasons. First, it can be because the browser just sent a GET request,
    which I need to respond
    by providing an initial version of the form template. It can also be when
    the browser sends
    a POST request with form data, but something in that data is invalid. For
    this form, I need to
    treat these two cases separately. When the form is being requested for the
    first time with a GET
    request, I want to pre-populate the fields with the data that is stored in
    the database, so I need to
    do the reverse of what I did on the submission case and move the data
    stored
    in the user fields
    to the form, as this will ensure that those form fields have the current
    data stored for the user.
    But in the case of a validation error I do not want to write anything to
    the
    form fields, because
    those were already populated by WTForms. To distinguish between these two
    cases, I check
    request.method , which will be GET for the initial request, and POST for a
    submission that
    failed validation.
    :return: edit_profile.html
    '''
    try:
        form = EditProfileForm(current_user.username)
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.about_me = form.about_me.data
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('user', username=current_user.username))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.about_me.data = current_user.about_me
            return render_template('edit_profile.html',
                                   title='Edit Profile', form=form)
    except Exception as e:
        logging.error(e)
        errors.internal_error(e)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
    return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            email.send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
