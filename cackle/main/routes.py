from flask import current_app
from cackle import db
from flask import render_template, flash, redirect, url_for, request
from .forms import EditProfileForm, EmptyForm, BlogForm
from flask_login import current_user, login_required
from cackle.models import User, Post
from datetime import datetime
from . import bp

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/')
@bp.route('/home', methods=['GET', 'POST'])
@login_required
def index():
    form = BlogForm()
    empty_form = EmptyForm()
    if form.validate_on_submit():
        blog_post = Post(body=form.body.data, user_id=current_user.id, timestamp=datetime.utcnow())
        db.session.add(blog_post)
        db.session.commit()
        flash('The post was made successfully', 'success')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', 
                            form=form,
                            posts=posts.items,
                            next_url=next_url,
                            prev_url=prev_url,
                            empty_form=empty_form)


@bp.route('/user/<username>')
@login_required
def user(username):
    form = EmptyForm()
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc())
    return render_template('user.html', user=user, posts=posts, form=form)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    empty_form = EmptyForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved', 'success')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username 
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form, empty_form=empty_form)



@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username} not found', 'secondary')
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(f'You cannot follow yourself', 'secondary')
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'Successfully followed User - {username}', 'success')
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username} not found', 'secondary')
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(f'You cannot unfollow yourself', 'secondary')
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'Successfully unfollowed User - {username}', 'success')
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))

@bp.route('/explore')
@login_required
def explore():
    empty_form = EmptyForm()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html',
                            title='Explore',
                            posts=posts.items,
                            next_url=next_url,
                            prev_url=prev_url,
                            empty_form=empty_form)


@bp.route('/delete_post/<post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    form = EmptyForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(id=post_id).first()
        if not post or post.user_id != current_user.id:
            flash('Unable to delete post', 'warning')
            return redirect(url_for('main.index'))
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully', 'success')
    return redirect(url_for('main.index'))