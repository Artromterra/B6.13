import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def save(year, artist, genre, album):
    assert isinstance(year, int), "Некорректная дата"
    assert isinstance(artist, str), "Не правильное название артиста"
    assert isinstance(genre, str), "Не верный жанр"
    assert isinstance(album, str), "Некорректное название альбома"

    session = connect_db()
    saved_album = session.query(Album).filter(Album.album == album, Album.artist == artist).first()
    if saved_album is not None:
        raise Exception("Альбом уже существует и записан под №{}".format(saved_album.id))
    album = Album(
        year=year,
        artist=artist,
        genre=genre,
        album=album
    )
    session.add(album)
    session.commit()
    return album

