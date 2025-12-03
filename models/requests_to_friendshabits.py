import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db.create_db import Habits, FriendsHabits, User, Friends
from .requests_to_friends import get_all_friends_by_user_id
from .requests_to_users import get_user_id_by_tg_id
from models.requests_to_log_habits import get_habit_marks_count
from .session import session


def get_all_requests_in_habits(tg_id: int):
    user_id = get_user_id_by_tg_id(tg_id)
    print(user_id)
    friends = get_all_friends_by_user_id(tg_id)
    friends_id = [fr.id for fr in friends]
    list_coop_habits = session.query(FriendsHabits).filter(FriendsHabits.friend_id.in_(friends_id)).filter(FriendsHabits.status=='waiting_habit', FriendsHabits.receiver_id==user_id).all()
    print([x.habit_id for x in list_coop_habits])
    return list_coop_habits


def update_status_coop_habit(habit_id: int, new_status: str) -> bool:
    try:
        coop_habit = session.query(FriendsHabits).filter(FriendsHabits.id==habit_id).first()
        coop_habit.status = new_status
        session.commit()
        return True
    except Exception as e:
        raise ValueError(e)

def create_coop_habit_invite(habit_id, friendship_id, receiver_id: int, sender_id: int):
    coop_habit = FriendsHabits(
        habit_id=habit_id,
        friend_id=friendship_id,
        receiver_id=receiver_id,
        sender_id=sender_id,
        status='waiting_habit'
    )
    session.add(coop_habit)
    session.commit()
    return coop_habit.id


def get_pending_coop_invites(user_tg_id):
    user = session.query(User).filter(User.tg_id == user_tg_id).first()
    if not user:
        return []

    friends_habits = session.query(FriendsHabits).filter(
        FriendsHabits.status == 'waiting_habit'
    ).all()

    invites = []
    for fh in friends_habits:
        friendship = session.query(Friends).filter(Friends.id == fh.friend_id).first()
        if not friendship:
            continue

        if friendship.fr1_id != user.id and friendship.fr2_id != user.id:
            continue

        habit = session.query(Habits).filter(Habits.id == fh.habit_id).first()
        if not habit:
            continue

        if friendship.fr1_id == user.id:
            sender_id = friendship.fr2_id
        else:
            sender_id = friendship.fr1_id

        sender = session.query(User).filter(User.id == sender_id).first()
        sender_name = f"User_{sender.tg_id}" if sender else "Неизвестный"

        invites.append({
            'id': fh.id,
            'habit_name': habit.name,
            'day_len': habit.day_len,
            'sender_name': sender_name
        })

    return invites


def accept_coop_habit(friends_habit_id, user_tg_id):
    friends_habit = session.query(FriendsHabits).filter(FriendsHabits.id == friends_habit_id).first()

    if not friends_habit:
        return None

    habit = session.query(Habits).filter(Habits.id == friends_habit.habit_id).first()
    if not habit:
        return None

    user = session.query(User).filter(User.tg_id == user_tg_id).first()

    if not user:
        return None

    new_habit = Habits(
        user_id=user.id,
        name=habit.name,
        day_len=habit.day_len,
        notification=habit.notification,
        is_coop='yes'
    )
    session.add(new_habit)
    session.commit()

    friends_habit.status = 'accepted'
    session.commit()

    return {
        'habit_name': habit.name,
        'success': True
    }


def reject_coop_habit(friends_habit_id):
    coop_habit = session.query(FriendsHabits).filter(FriendsHabits.id == friends_habit_id).first()
    if coop_habit:
        coop_habit.status = 'rejected'
        session.commit()
        return {'success': True}
    return {'success': False}


def get_coop_progress(habit_id, user_tg_id):
    habit = session.query(Habits).filter(Habits.id == habit_id).first()
    if not habit:
        return None

    coop_habit = session.query(FriendsHabits).filter(
        FriendsHabits.habit_id == habit_id
    ).first()

    if not coop_habit:
        return None

    friendship = session.query(Friends).filter(Friends.id == coop_habit.friend_id).first()
    if not friendship:
        return None

    current_user = session.query(User).filter(User.tg_id == user_tg_id).first()
    if not current_user:
        return None

    if friendship.fr1_id == current_user.id:
        friend_user_id = friendship.fr2_id
    else:
        friend_user_id = friendship.fr1_id

    friend_user = session.query(User).filter(User.id == friend_user_id).first()
    if not friend_user:
        return None

    friend_habit = session.query(Habits).filter(
        Habits.user_id == friend_user_id,
        Habits.name == habit.name,
        Habits.is_coop == 'yes'
    ).first()

    if not friend_habit:
        return None


    user_marks = get_habit_marks_count(habit_id)
    friend_marks = get_habit_marks_count(friend_habit.id)

    def create_progress_bar(days_completed, total_days):
        filled = min(days_completed, total_days)
        empty = total_days - filled
        return '█' * filled + '∙' * empty

    user_progress_bar = create_progress_bar(user_marks, habit.day_len)
    friend_progress_bar = create_progress_bar(friend_marks, habit.day_len)

    from models.requests_to_friends import get_friend_name_by_tg_id
    import asyncio

    friend_name = "Друг"
    days_remaining = max(0, habit.day_len - max(user_marks, friend_marks))

    return {
        'habit_name': habit.name,
        'duration': habit.day_len,
        'user_days': user_marks,
        'friend_days': friend_marks,
        'user_progress_bar': user_progress_bar,
        'friend_progress_bar': friend_progress_bar,
        'friend_name': friend_name,
        'total_days': user_marks + friend_marks,
        'total_duration': habit.day_len * 2,
        'days_remaining': days_remaining
    }