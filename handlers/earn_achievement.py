from aiogram.types import BufferedInputFile
import os
from models.requests_to_ach import award_achievement, get_achievement_by_id
from models.requests_to_habits import get_all_habits_by_user_id
from models.requests_to_users import get_user_id_by_tg_id
from models.requests_to_friends import get_all_friends_by_user_id
from models.requests_to_log_habits import get_habits_marks

class EarnAchievement:

    @staticmethod
    def check_habit_achievements(tg_id: int) -> list:
        user_id = get_user_id_by_tg_id(tg_id)
        habits = get_all_habits_by_user_id(tg_id)
        habit_count = len(habits)

        awarded_achievements = []

        if habit_count == 1:
            if award_achievement(user_id, 1):
                awarded_achievements.append(1)

        if habit_count == 5:
            if award_achievement(user_id, 2):
                awarded_achievements.append(2)

        return awarded_achievements

    @staticmethod
    def check_friend_achievement(tg_id: int) -> list:
        user_id = get_user_id_by_tg_id(tg_id)
        friends = get_all_friends_by_user_id(tg_id)
        friends_count = len(friends)

        awarded_achievements = []

        if friends_count == 1:
            if award_achievement(user_id, 3):
                awarded_achievements.append(3)

        if friends_count == 5:
            if award_achievement(user_id, 4):
                awarded_achievements.append(4)

        if friends_count == 10:
            if award_achievement(user_id, 5):
                awarded_achievements.append(5)

        return awarded_achievements

    @staticmethod
    def check_mark_achievements(tg_id: int, habit_id: int) -> list:
        user_id = get_user_id_by_tg_id(tg_id)
        marks = get_habits_marks(habit_id)
        marks_count = len(marks)

        awarded_achievements =[]

        if marks_count >= 7:
            if award_achievement(user_id, 6):
                awarded_achievements.append(6)

        if marks_count >= 60:
            if award_achievement(user_id, 7):
                awarded_achievements.append(7)

        if marks_count >= 180:
            if award_achievement(user_id, 8):
                awarded_achievements.append(8)

        if marks_count >= 365:
            if award_achievement(user_id, 9):
                awarded_achievements.append(9)

        return awarded_achievements

    @staticmethod
    def get_achievement_image(achievement):
        if achievement.img and os.path.exists(achievement.img):
            with open(achievement.img, 'rb') as f:
                image_data = f.read()

            return BufferedInputFile(image_data, filename=achievement.img)
        return None

    @staticmethod
    def get_achievement_by_id(achievement_id: int):
        return get_achievement_by_id(achievement_id)
