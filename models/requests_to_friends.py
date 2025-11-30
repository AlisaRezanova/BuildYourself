import os
from aiogram import Bot
from decouple import config
from sqlalchemy import create_engine, or_, and_, delete
from sqlalchemy.orm import sessionmaker
from create_db.create_db import Friends, User
from models.exceptions import FriendsNotAdded
from datetime import date
from models.requests_to_users import get_user_id_by_tg_id
from .session import session


def get_all_friends_by_user_id(tg_id: int) -> list:
    user_id = get_user_id_by_tg_id(tg_id)
    friends = session.query(Friends).filter(or_(Friends.fr1_id==user_id, Friends.fr2_id==user_id)).filter(Friends.status=='accept').all()
    friends = list(set(friends))
    return friends


def add_note_friends(tg_id: int, invite_code: str) -> bool:
    user_id = get_user_id_by_tg_id(tg_id)
    new_friends = Friends(
        invite_code=invite_code,
        fr1_id = user_id
    )
    try:
        session.add(new_friends)
        session.commit()
        return True
    except Exception:
        raise FriendsNotAdded('friends not added')


def update_friends2(tg_id: int, invite_code) -> bool:
    user_id = get_user_id_by_tg_id(tg_id)
    friends = session.query(Friends).filter(and_(Friends.invite_code == invite_code, Friends.fr2_id.is_(None))).first()
    if friends:
        friends.fr2_id = user_id
        friends.start_friendship = date.today()
        session.commit()
        return True
    else:
        return False



def check_eq_invite_code(invite_code: str):
    from handlers.friends import generate_invite_code
    friends = session.query(Friends).all()
    codes = [fr.invite_code for fr in friends]
    if invite_code in codes:
        generate_invite_code()
    else:
        return invite_code


def update_fr_status(status: str, fr_id: int) -> bool:
    friend = session.query(Friends).filter(Friends.id == fr_id).first()
    if friend:
        friend.status = status
        session.commit()
        return True
    else:
        return False


def get_all_requests(tg_id: int) -> list:
    user_id = get_user_id_by_tg_id(tg_id)
    requests = session.query(Friends).filter(Friends.fr1_id == user_id).filter(Friends.status == 'Waiting').filter(Friends.fr2_id != None).all()
    return requests


def delete_friend_by_id(fr_id: int):
    try:
        stmt = (delete(Friends).where(Friends.id == fr_id))
        session.execute(
            stmt)
        session.commit()
    except:
        raise ValueError('Error')



async def get_friend_name_by_tg_id(tg_id):
    try:
        bot = Bot(token=config('TOKEN'))
        user_chat = await bot.get_chat(tg_id)
        await bot.session.close()

        if user_chat.first_name:
            if user_chat.last_name:
                return f"{user_chat.first_name} {user_chat.last_name}"
            return user_chat.first_name
        elif user_chat.username:
            return f"@{user_chat.username}"
        else:
            return f"User_{tg_id}"

    except Exception as e:
        print(f"Error getting friend name: {e}")
        return f"User_{tg_id}"


async def get_friends_list_with_names(user_tg_id):
    try:

        user = session.query(User).filter(User.tg_id == user_tg_id).first()
        if not user:
            return []

        friends_as_fr1 = session.query(Friends).filter(
            Friends.fr1_id == user.id,
            Friends.status == 'accept'
        ).all()

        friends_as_fr2 = session.query(Friends).filter(
            Friends.fr2_id == user.id,
            Friends.status == 'accept'
        ).all()

        friends_list = []


        for friend in friends_as_fr1:
            friend_user = session.query(User).filter(User.id == friend.fr2_id).first()
            if friend_user:
                friend_name = await get_friend_name_by_tg_id(friend_user.tg_id)
                friends_list.append({
                    'id': friend.id,
                    'user_id': friend_user.id,
                    'tg_id': friend_user.tg_id,
                    'name': friend_name
                })


        for friend in friends_as_fr2:
            friend_user = session.query(User).filter(User.id == friend.fr1_id).first()
            if friend_user:
                friend_name = await get_friend_name_by_tg_id(friend_user.tg_id)
                friends_list.append({
                    'id': friend.id,
                    'user_id': friend_user.id,
                    'tg_id': friend_user.tg_id,
                    'name': friend_name
                })

        return friends_list

    except Exception as e:
        print(f"Error getting friends list: {e}")
        return []
    finally:
        session.close()

def get_friendship_by_id(friendship_id):
    friendship = session.query(Friends).filter(Friends.id == friendship_id).first()
    return friendship



