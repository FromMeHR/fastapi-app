from fastapi import APIRouter, Body, Depends, HTTPException, Path, Request
from app.forms import UserLoginForm, UserCreateForm, PostCreateForm
from app.models import User, Post
from app.utils import get_password_hash
from app.jwt_settings import encode_token, decode_token
from app.connection import session
from starlette import status

router = APIRouter()

@router.get('/')
def index():
    return {'success': True}

def get_request_user(request: Request):
    if 'token' in request.session:
        token_data = decode_token(request.session['token'])
        if 'user_id' in token_data:
            user_id = token_data['user_id']
            user = session.query(User).filter(User.id == user_id).first()
            return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or missing token')

@router.post('/login')
def login(request: Request, user_form: UserLoginForm = Body(..., embed=True)):
    user = session.query(User).filter(User.email == user_form.email, User.password == get_password_hash(user_form.password)).first()
    if user is not None:
        auth_token = encode_token(user.id)
        user.auth_key = auth_token
        session.commit()
        request.session['token'] = encode_token(user.id)
        return {'success': True, 'token': request.session.get('token')}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid data')

@router.post('/logout')
def logout(request: Request):
    if 'token' in request.session:
        user = get_request_user(request)
        if user:
            user.auth_key = None
            session.commit()
        request.session.clear()
        return {'success': 'Logout successful'}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or missing token')

@router.post('/create_user')
def create_user(user: UserCreateForm = Body(..., embed=True)):
    exist_user = session.query(User.id).filter(User.email == user.email).first()
    if exist_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')
    new_user = User(email=user.email,
                    password=get_password_hash(user.password),
                    first_name=user.first_name,
                    last_name=user.last_name)
    session.add(new_user)
    session.commit()
    return {'user_id': new_user.id}

@router.post('/change_password')
def change_password(request: Request, old_password: str = Body(...), new_password: str = Body(...), user: User = Depends(get_request_user)):
    if user.password == get_password_hash(old_password):
        user.password = get_password_hash(new_password)
        session.commit()
        return {'success': 'Password changed successfully'}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid old password')

@router.post('/create_post')
def create_post(post: PostCreateForm = Body(..., embed=True), user: User = Depends(get_request_user)):
    new_post = Post(title=post.title, topic=post.topic, user_id=user.id)
    session.add(new_post)
    session.commit()
    return {'post_id': new_post.id, 'title': new_post.title, 'topic': new_post.topic}

@router.get('/get_post/{post_id}')
def get_post(post_id: int = Path(...), user: User = Depends(get_request_user)):
    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    if user.id != post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can\'t watch this post')
    return post

@router.get('/get_posts')
def get_posts(user: User = Depends(get_request_user)):
    posts = session.query(Post).filter(Post.user_id == user.id).all()
    return posts


@router.delete('/delete_post/{post_id}')
def delete_post(post_id: int = Path(...), user: User = Depends(get_request_user)):
    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    if user.id != post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can\'t delete this post')
    session.delete(post)
    session.commit()
    return {'success': 'Post deleted successfully'}

@router.put('/update_post/{post_id}')
def update_post(post_id: int = Path(...), updated_post: PostCreateForm = Body(..., embed=True), user: User = Depends(get_request_user)):
    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    if user.id != post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can\'t update this post')
    post.title = updated_post.title
    post.topic = updated_post.topic
    session.commit()
    session.refresh(post)
    return {'success': 'Post updated successfully'}

@router.put('/status/{post_id}')
def status_post(post_id: int = Path(...), user: User = Depends(get_request_user)):
    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    if user.id != post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can\'t update the status of this post')
    post.status = not post.status
    session.commit()
    session.refresh(post)
    return {'success': 'Post status updated successfully'}