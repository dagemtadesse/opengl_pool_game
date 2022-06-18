import numpy as np

NEAR = 0.005
ZERO = 0.00001

class MotionController():
    def __init__(self, balls):
        self.x_min = -1.5
        self.x_max = 1.5
        
        self.z_min = -5.07
        self.z_max = -2.93
        
        self.y_min = 0
        self.y_max = 0

        self.balls = balls
        
        self.deaccleration = np.array((0.99, 0.99, 0.99))

    def updatePosition(self):
        for ball in self.balls:
            
            if not np.all(ball.velocity == 0):
                ball.rotate()
                # print(ball.position)
                
                ball.position = np.add(
                    ball.position, ball.velocity).reshape((3,))
                
                x, y, z  = ball.position               
                vx, vy, vz = ball.velocity
                
                if x <= self.x_min or x >= self.x_max:
                    vx = -vx
                    if x < self.x_min: x = self.x_min
                    if x > self.x_max: x = self.x_max
                
                if y <= self.x_min or  y >= self.x_max:
                    vy = -vy
                    if y < self.y_min: y = self.y_min
                    if y > self.y_max: y = self.y_max
                    
                if z <= self.x_min or  z >= self.x_max:
                    vz = -vz
                    if z < self.z_min: z = self.z_min
                    if z > self.z_max: z = self.z_max
                
                ball.velocity = np.array([vx, vy, vz]) * self.deaccleration
                
                for otherBall in self.balls:
                    # detect collision with other balls
                    if otherBall is ball:
                        continue
                    
                    direction = ball.position - otherBall.position
                    distance = np.linalg.norm(direction)
                    if distance <= NEAR :
                        velocity = direction / distance
                        otherBall.velocity = velocity * ball.velocity
                        ball.velocity -= otherBall.velocity
    
    def updatePoolCue(self, poolCue, cueBall):
        if not all(abs(i) <= ZERO for i in cueBall.velocity):
            poolCue.position = np.array([0, 0, 1])
        else:
            poolCue.position = cueBall.position
                      