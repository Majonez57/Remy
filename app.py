import json
import os
from PIL import Image

from flask import Flask, request
import torch

app = Flask(__name__)

recipe_directory = './recipes'

recipes = []

model = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt', force_reload=True)


def initialise():
    for filename in os.listdir(recipe_directory):
        with open(os.path.join(recipe_directory, filename)) as file:
            recipe = json.load(file)
            recipe['tags'] = set(recipe['tags'])
            recipes.append(recipe)
    model.eval()


@app.get("/recipes")
def recipes_list():
    tags = set(request.args.getlist('tags'))

    out = []
    for i, r, n in sorted(((index, recipe, len(tags.intersection(recipe['tags']))) for index, recipe in enumerate(recipes)), key=lambda x : x[2], reverse=True):
        if n > 0:
            out.append(dict(title=r['title'], shortDescription=r['description'][:50] + "...", imageSrc=r['imageSrc'], id=i + 1))

    print(out)

    return out


@app.get("/recipes/<id>")
def recipes_member(id):
    out = recipes[int(id) - 1].copy()
    del out['tags']
    return out

@app.post('/tags')
def upload_file():
    out = model(list(Image.open(f) for f in request.files.values()))

    outout = out.pandas().xyxy[0]['name'].unique().tolist()
    print(outout)
    return outout


initialise()
