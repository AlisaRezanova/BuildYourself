import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db.create_db import Achievements

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'buildyourself.db'))

engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)


def init_achievements():
    achievements_data = [
        {
            'id': 1,
            'name': 'Первый шаг',
            'img': 'img/for_achievements/1.png',
            'description': 'Ввести первую привычку'
        },
        {
            'id': 2,
            'name': 'На полную мощность',
            'img': 'img/for_achievements/2.png',
            'description': 'Ввести пятую привычку'
        },
        {
            'id': 3,
            'name': 'Первый союзник',
            'img': 'img/for_achievements/3.png',
            'description': 'Добавить первого друга'
        },
        {
            'id': 4,
            'name': 'Рука помощи',
            'img': 'img/for_achievements/4.png',
            'description': 'Добавить пятого друга'
        },
        {
            'id': 5,
            'name': 'Душа компании',
            'img': 'img/for_achievements/5.png',
            'description': 'Добавить десятого друга'
        },
        {
            'id': 6,
            'name': 'Уверенный старт',
            'img': 'img/for_achievements/6.png',
            'description': 'Отметить привычку 1 неделю'
        },
        {
            'id': 7,
            'name': 'Железная воля',
            'img': 'img/for_achievements/7.png',
            'description': 'Отметить привычку 2 месяца'
        },
        {
            'id': 8,
            'name': 'Адепт дисциплины',
            'img': 'img/for_achievements/8.png',
            'description': 'Отметить привычку 6 месяцев'
        },
        {
            'id': 9,
            'name': 'Мастер',
            'img': 'img/for_achievements/9.png',
            'description': 'Отметить привычку 1 год'
        }
    ]

    with Session() as session:
        for achievement_data in achievements_data:
            existing = session.query(Achievements).filter(Achievements.id == achievement_data['id']).first()
            if not existing:
                achievement = Achievements(
                    id=achievement_data['id'],
                    name=achievement_data['name'],
                    img=achievement_data['img'],
                    description=achievement_data['description']
                )
                session.add(achievement)
            else: # Потом обновить пути к картинкам или названия наград при необходимости
                existing.img = achievement_data['img']
                existing.description = achievement_data['description']

        session.commit()
    print("Награды инициализированы!")


if __name__ == "__main__":
    init_achievements()
