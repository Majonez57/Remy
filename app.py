import json
import os

from flask import Flask, request

app = Flask(__name__)

recipe_directory = './recipes'

recipes = []


def initialise():
    for filename in os.listdir(recipe_directory):
        with open(os.path.join(recipe_directory, filename)) as file:
            recipe = json.load(file)
            recipe['tags'] = set(recipe['tags'])
            recipes.append(recipe)
    print(recipes)


@app.get("/recipes")
def recipes_list():
    tags = set(request.args.getlist('tags'))

    out = []
    for i, r, n in ((index, recipe, len(tags.intersection(recipe['tags'])) > 0) for index, recipe in enumerate(recipes)):
        if n > 0:
            out.append(dict(title=r['title'], shortDescription=r['description'][:50] + "...", imageSrc="", id=i + 1))

    print(out)

    return out


@app.get("/recipes/<id>")
def recipes_member(id):
    out = recipes[int(id) - 1].copy()
    del out['tags']
    return out


initialise()
