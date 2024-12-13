from flask import Flask, jsonify, request
from config import Config
from models import db, Actor, Film, FilmActor

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


@app.route("/")
def hello_world():
    return "Hola Mundo"


@app.route("/actors")
def get_actors():
    actors = Actor.query.all()
    # result = [{"actor_id": actor.actor_id, "first_name": actor.first_name, "last_name": actor.last_name} for actor in actors]
    result = [actor.to_dict() for actor in actors]
    return jsonify(result)


@app.route("/actors", methods=["POST"])
def create_actor():
    data = request.get_json()
    new_actor = Actor(first_name=data["first_name"], last_name=data["last_name"])
    db.session.add(new_actor)
    db.session.commit()
    return jsonify({"message": "Actor creado", "actor_id": new_actor.actor_id})


@app.route("/actors/bulk", methods=["POST"])
def create_actors_bulk():
    data = request.get_json()
    actors = [
        Actor(first_name=actor["first_name"], last_name=actor["last_name"])
        for actor in data
    ]
    db.session.add_all(actors)
    db.session.commit()
    return jsonify({"message": f"{len(actors)} actores creados"})


# Obtener todas las películas
@app.route("/films", methods=["GET"])
def get_films():
    films = Film.query.all()
    # result = [{"film_id": film.film_id, "title": film.title, "description": film.description, "release_year": film.release_year} for film in films]
    result = [film.to_dict() for film in films]  # Usamos el método to_dict()
    return jsonify(result)


# Crear una película
@app.route("/films", methods=["POST"])
def create_film():
    data = request.get_json()
    new_film = Film(
        title=data["title"],
        description=data["description"],
        release_year=data["release_year"],
    )
    db.session.add(new_film)
    db.session.commit()
    return jsonify({"message": "Película creada", "film_id": new_film.film_id})


# Asociar un actor a una película
@app.route("/actors/<int:actor_id>/films/<int:film_id>", methods=["POST"])
def associate_actor_film(actor_id, film_id):
    association = FilmActor(actor_id=actor_id, film_id=film_id)
    db.session.add(association)
    db.session.commit()
    return jsonify({"message": f"Actor {actor_id} asociado a película {film_id}"})


# Traer todas las películas con sus actores
@app.route("/films/actors", methods=["GET"])
def get_films_with_actors():
    films = Film.query.all()
    result = []
    for film in films:
        actors = (
            db.session.query(Actor)
            .join(FilmActor)
            .filter(FilmActor.film_id == film.film_id)
            .all()
        )
        result.append(
            {
                "film_id": film.film_id,
                "title": film.title,
                "actors": [
                    {
                        "actor_id": actor.actor_id,
                        "name": f"{actor.first_name} {actor.last_name}",
                    }
                    for actor in actors
                ],
            }
        )
    return jsonify(result)


# Actualizar una película
@app.route("/films/<int:film_id>", methods=["PUT"])
def update_film(film_id):
    film = Film.query.get(film_id)
    if not film:
        return jsonify({"error": "Película no encontrada"}), 404
    data = request.get_json()
    film.title = data.get("title", film.title)
    film.description = data.get("description", film.description)
    film.release_year = data.get("release_year", film.release_year)
    db.session.commit()
    return jsonify({"message": "Película actualizada"})


# Eliminar una película
@app.route("/films/<int:film_id>", methods=["DELETE"])
def delete_film(film_id):
    film = Film.query.get(film_id)
    if not film:
        return jsonify({"error": "Película no encontrada"}), 404
    db.session.delete(film)
    db.session.commit()
    return jsonify({"message": "Película eliminada"})


# Traer actores de una película específica
@app.route("/films/<int:film_id>/actors", methods=["GET"])
def get_film_actors(film_id):
    actors = (
        db.session.query(Actor)
        .join(FilmActor)
        .filter(FilmActor.film_id == film_id)
        .all()
    )
    result = [
        {"actor_id": actor.actor_id, "name": f"{actor.first_name} {actor.last_name}"}
        for actor in actors
    ]
    return jsonify(result)


# Traer un actor con sus películas
@app.route("/actors/<int:actor_id>/films", methods=["GET"])
def get_actor_with_films(actor_id):
    films = (
        db.session.query(Film)
        .join(FilmActor)
        .filter(FilmActor.actor_id == actor_id)
        .all()
    )
    result = [{"film_id": film.film_id, "title": film.title} for film in films]
    return jsonify(result)


if __name__ == "__main__":
    app.run(port=3000)
