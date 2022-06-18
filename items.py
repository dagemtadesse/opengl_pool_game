import numpy as np
import random
from model_mesh import Model, ModelMesh
from texture import Material


poolCue = Model(
    position=[0, 0, -4],
    eulers=[60, 0, 0],
    mesh=ModelMesh("models/inverted_que.obj"),
    texture=Material('textures/pool_cue.jpg')
)

table = Model(
    position=[0, 0, -4],
    eulers=[0, 0, 0],
    mesh=ModelMesh("models/table.obj"),
    texture=Material('textures/leather.jpg')
)

plane = Model(
    position=[0, 0, -4],
    eulers=[0, 0, 0],
    mesh=ModelMesh("models/plane.obj"),
    texture=Material('textures/felt.bmp')
)


balls = [
    Model(
        position=[random.uniform(-1.25, 1.25), 0.02, -3.9],
        eulers=[0, 0.02, 0, ],
        mesh=ModelMesh("models/ball.obj"),
        texture=Material(f'textures/{i}.png')
    ) for i in range(1, 2)
]

whiteBall = Model(
    position=[0, 0.02, -3.9],
    eulers=[0, 0, 0, ],
    mesh=ModelMesh("models/ball.obj"),
    texture=Material('textures/BallCue.jpg')
)
