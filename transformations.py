import numpy as np
import pyrr

tableTransformation = [
    pyrr.matrix44.create_from_x_rotation(theta=np.radians(-45)),
]

def cueTransformation(cueBall, targetBall):
    cuePos = np.array(cueBall.position)
    targetPos = np.array(targetBall.position)
    stickPos = np.array([0, 1, 0])

    directionVec = targetPos - cuePos
    directionVec /= np.linalg.norm(directionVec)

    angle = np.arccos(np.dot(directionVec, stickPos))
    axis = np.cross(directionVec, stickPos)

    return[
        pyrr.matrix44.create_from_axis_rotation(
            axis=axis, theta=angle),
        # pyrr.matrix44.create_from_z_rotation(theta=np.radians(45)),
    ]
