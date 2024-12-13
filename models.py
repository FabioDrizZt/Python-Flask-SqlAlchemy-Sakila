from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Actor(db.Model):
    __tablename__ = "actor"
    actor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)

    def to_dict(self):
        return {
            "actor_id": self.actor_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }


class Film(db.Model):
    __tablename__ = "film"
    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    release_year = db.Column(db.Integer)

    def to_dict(self):
        return {
            "film_id": self.film_id,
            "title": self.title,
            "description": self.description,
            "release_year": self.release_year,
        }


class FilmActor(db.Model):
    __tablename__ = "film_actor"
    actor_id = db.Column(db.Integer, db.ForeignKey("actor.actor_id"), primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey("film.film_id"), primary_key=True)
