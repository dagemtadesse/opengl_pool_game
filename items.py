import numpy as np
import pyrr
from model_mesh import Model, ModelMesh
from texture import Material


poolCue = Model(
    position=[0, 0, -3],
    eulers=[0, 0, 0, ],
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

ball8 = Model(
    position=[-0.25, 0, -3],
    eulers=[0, 0, 0, ],
    mesh=ModelMesh("models/ball.obj"),
    texture=Material('textures/8.png')
)

whiteBall = Model(
    position=[0, 0, -3],
    eulers=[0, 0, 0, ],
    mesh=ModelMesh("models/ball.obj"),
    texture=Material('textures/BallCue.jpg')
)


