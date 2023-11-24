from fastapi import APIRouter, Body, Depends, HTTPException, Path
from app.forms import UserLoginForm, UserCreateForm, PostCreateForm
from app.models import connect_db, User, Post, AuthToken
from app.utils import get_password_hash
from starlette import status
import uuid

router = APIRouter()

@router.get('/')
def index():
    return {'success': True}

def check_auth_token(token: str, database=Depends(connect_db)): # get_user get_post create_post...
    auth_token = database.query(AuthToken).filter(AuthToken.token == token).one_or_none()
    if auth_token:
        return auth_token
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Auth error')

@router.post('/login')
def login(user_form: UserLoginForm = Body(..., embed=True), database=Depends(connect_db)):
    user = database.query(User).filter(User.email == user_form.email).one_or_none()
    if not user or get_password_hash(user_form.password) != user.password:
        return {'error': 'Email/password invalid'}
    auth_token = AuthToken(token=str(uuid.uuid4()), user_id=user.id)
    database.add(auth_token)
    database.commit()
    return {'auth_token': auth_token.token}

@router.post('/logout')
def logout(token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
    auth_token_obj = database.query(AuthToken).filter(AuthToken.token == token.token).one_or_none()
    if auth_token_obj:
        database.delete(auth_token_obj)
        database.commit()
        return {'success': 'Logout successful'}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid auth token')

@router.post('/create_user')
def create_user(user: UserCreateForm = Body(..., embed=True), database=Depends(connect_db)):
    exist_user = database.query(User.id).filter(User.email == user.email).one_or_none()
    if exist_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')
    new_user = User(email=user.email,
                    password=get_password_hash(user.password),
                    first_name=user.first_name,
                    last_name=user.last_name)
    database.add(new_user)
    database.commit()
    return {'user_id': new_user.id}

@router.post('/create_post')
def create_post(post: PostCreateForm = Body(..., embed=True), token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
    user = database.query(User).filter(User.id == token.user_id).one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    new_post = Post(title=post.title, topic=post.topic, user_id=user.id)
    database.add(new_post)
    database.commit()
    return {'post_id': new_post.id, 'title': new_post.title, 'topic': new_post.topic}

@router.get('/get_post/{post_id}')
def get_post(post_id: int = Path(...), database=Depends(connect_db), token: AuthToken = Depends(check_auth_token)):
    post = database.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    if token.user_id != post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can\'t watch this post')
    return post

@router.get('/get_posts')
def get_posts(token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
    posts = database.query(Post).filter(Post.user_id == token.user_id).all()
    return posts


@router.delete('/delete_post/{post_id}')
def delete_post(post_id: int = Path(...), token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
    post = database.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    if token.user_id != post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can\'t delete this post')
    database.delete(post)
    database.commit()
    return {'success': 'Post deleted successfully'}

@router.put('/update_post/{post_id}')
def update_post(post_id: int = Path(...), updated_post: PostCreateForm = Body(..., embed=True), token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
    post = database.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    if token.user_id != post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can\'t update this post')
    post.title = updated_post.title
    post.topic = updated_post.topic
    database.commit()
    return {'success': 'Post updated successfully'}

@router.put('/status/{post_id}')
def status_post(post_id: int = Path(...), token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
    post = database.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    if token.user_id != post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can\'t update the status of this post')
    post.status = not post.status
    database.commit()
    return {'success': 'Post status updated successfully'}