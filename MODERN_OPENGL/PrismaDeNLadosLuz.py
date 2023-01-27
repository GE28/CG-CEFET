from GLAPP import GLAPP
from OpenGL import GL
from array import array
import ctypes
import glm
import math
a = 0
SIDES = 3
HEIGHT = 2

class Prism(GLAPP):

    def setup(self):
        self.title("Prisma")
        self.size(800,800)

        GL.glClearColor(0.2, 0.2, 0.2, 0.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)

        self.pipeline = self.loadPipeline("SimpleLightning")
        GL.glUseProgram(self.pipeline)

        self.prismArrayBufferId = None
        self.prismHeightArrayBufferId = None

    def drawPrism(self):
        def getCirclePoint(side, height=0):
            return [math.cos(2*math.pi*side/SIDES),height,math.sin(2*math.pi*side/SIDES)]

        trianglePositions = array('f')
        triangleColorCodes = array('f')
        normalVectors = array('f', [])

        if self.prismArrayBufferId == None:
            for side in range(SIDES):
                trianglePositions.extend([0,0,0])
                trianglePositions.extend(getCirclePoint(side))
                trianglePositions.extend(getCirclePoint(side+1))

            for i in range(0, len(trianglePositions), 3):
                trianglePositions.extend([trianglePositions[i],HEIGHT,trianglePositions[i+2]])

            color = 0
            for side in range(SIDES):
                current = [0, 0, 0]
                current[color] = 0.7
                color = (color + 1) % 3
                for i in range(3):
                    triangleColorCodes.extend(current)

            for i in range(0, len(triangleColorCodes), 3):
                triangleColorCodes.extend(triangleColorCodes[i:i+3])

            for i in range(0, len(trianglePositions), 3):
                n = glm.normalize(glm.vec3(trianglePositions[i],trianglePositions[i+1],trianglePositions[i+2]))
                normalVectors.append(n.x)
                normalVectors.append(n.y)
                normalVectors.append(n.z)

            self.prismArrayBufferId = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.prismArrayBufferId)
            GL.glEnableVertexAttribArray(0)
            GL.glEnableVertexAttribArray(1)
            
            idVertexBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(trianglePositions)*trianglePositions.itemsize, ctypes.c_void_p(trianglePositions.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idColorBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idColorBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(triangleColorCodes)*triangleColorCodes.itemsize, ctypes.c_void_p(triangleColorCodes.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(1,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idNormalBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idNormalBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(normalVectors)*normalVectors.itemsize, ctypes.c_void_p(normalVectors.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(2,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))
            
        if self.prismHeightArrayBufferId == None:
            basePositions = array('f')
            colorCodes = array('f')
            normalVectors = array('f', [])
            
            for side in range(SIDES):
                basePositions.extend(getCirclePoint(side))             
                basePositions.extend(getCirclePoint(side+1))     
                basePositions.extend(getCirclePoint(side+1, HEIGHT))
                basePositions.extend(getCirclePoint(side, HEIGHT))       

            color = 0
            for _ in range(0, len(basePositions), 3):
                current = [0, 0, 0]
                current[color] = 0.6
                color = (color + 1) % 3
                for i in range(4):
                    colorCodes.extend(current)

            for i in range(0, len(trianglePositions), 3):
                n = glm.normalize(glm.vec3(trianglePositions[i],trianglePositions[i+1],trianglePositions[i+2]))
                normalVectors.append(n.x)
                normalVectors.append(n.y)
                normalVectors.append(n.z)
                
            self.prismHeightArrayBufferId = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.prismHeightArrayBufferId)
            GL.glEnableVertexAttribArray(0)
            GL.glEnableVertexAttribArray(1)
            
            idVertexBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(basePositions)*basePositions.itemsize, ctypes.c_void_p(basePositions.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idColorBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idColorBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(colorCodes)*colorCodes.itemsize, ctypes.c_void_p(colorCodes.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(1,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idNormalBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idNormalBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(normalVectors)*normalVectors.itemsize, ctypes.c_void_p(normalVectors.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(2,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))
        
        viewPos = glm.vec3(7,3,7)
        GL.glUniform3fv(GL.glGetUniformLocation(self.pipeline, "viewPos"), 1, glm.value_ptr(viewPos))

        lightPosition = glm.rotate(a,glm.vec3(0, 1, 0)) * glm.rotate(a/2,glm.vec3(1, 0, 0)) * glm.vec3(5.0,5.0,5.0)
        GL.glUniform3fv(GL.glGetUniformLocation(self.pipeline, "lightPosition"), 1, glm.value_ptr(lightPosition))

        projection = glm.perspective(math.pi/4,self.width/self.height,0.1,100)
        camera = glm.lookAt(viewPos,glm.vec3(0,0,0),glm.vec3(0,1,0))
        model = glm.rotate(a,glm.vec3(0, 1, 0)) * glm.rotate(a/2,glm.vec3(0, 0, 1)) * glm.rotate(a/2, glm.vec3(1, 0, 0))
        mvp = projection * camera * model
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipeline, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mvp))
        GL.glBindVertexArray(self.prismArrayBufferId)
        GL.glDrawArrays(GL.GL_TRIANGLES,0,SIDES * 3 * 2)

        GL.glBindVertexArray(self.prismHeightArrayBufferId)
        GL.glDrawArrays(GL.GL_QUADS,0,SIDES * 4)

    def draw(self):
        global a
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)

        self.drawPrism()
        a += 0.01

Prism()
