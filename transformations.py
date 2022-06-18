import numpy as np
import pyrr

tableTransformation = []

def cueTransformation(cueBall, targetBall):
    cuePos = cueBall.position
    targetPos = targetBall.position
    stickPos = np.array([0, 1, 0])

    directionVec = targetPos - cuePos
    directionVec /= np.linalg.norm(directionVec)

    angle = np.arccos(np.dot(directionVec, stickPos))
    axis = np.cross(directionVec, stickPos)
    # print("axis", directionVec.shape)

    return[
        pyrr.matrix44.create_from_axis_rotation(
            axis=axis, theta=angle),
    ]
