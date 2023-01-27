from GLAPP import GLAPP
from OpenGL import GL
from array import array
from numpy import interp
import ctypes
import glm
import math
a = 0
SIDES = 100
RADIUS = 2

class Solid(GLAPP):

    def setup(self):
        self.title("Solido")
        self.size(800,800)

        GL.glClearColor(0.2, 0.2, 0.2, 0.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)

        self.pipeline = self.loadPipeline("Blinn")
        GL.glUseProgram(self.pipeline)

        GL.glActiveTexture(GL.GL_TEXTURE0)
        textureSlot = self.loadTexture("./textures/uv_grid_opengl.png")
        GL.glBindTexture(GL.GL_TEXTURE_2D, textureSlot)

        lightPosition = glm.vec3(10.0,5.0,0)
        GL.glUniform3fv(GL.glGetUniformLocation(self.pipeline, "lightPosition"), 1, glm.value_ptr(lightPosition))

        self.solidArrayBufferId = None

    def drawSolid(self):
        def addVextexToList(list, vertex):
            for v in vertex:
                list.append(v)

        def getCirclePoint(i, j):
            lat = interp(i,[0,SIDES],[-math.pi/2,math.pi/2])
            lon = interp(j,[0,SIDES],[-math.pi,math.pi])
            return math.cos(lat)*math.sin(lon), math.sin(lat)*math.sin(lon), math.cos(lon)
            
        def getTextureVector(i, j):
            return i/SIDES, j/SIDES

        def getNormalVector(v):
            n = glm.normalize(v)
            return n.x, n.y, n.z

        if self.solidArrayBufferId == None:
            solidPositions = array('f', [])
            textureCoords = array('f', [])
            normalVectors = array('f', [])

            for i in range(SIDES):           
                for j in range(SIDES):
                    vA = getCirclePoint(i,j)
                    vB = getCirclePoint(i,j+1)
                    vC = getCirclePoint(i+1,j+1)
                    vD = getCirclePoint(i+1,j)

                    addVextexToList(solidPositions, vA)
                    addVextexToList(solidPositions, vB)
                    addVextexToList(solidPositions, vC)
                    addVextexToList(solidPositions, vD)

                    addVextexToList(textureCoords, getTextureVector(i, j))
                    addVextexToList(textureCoords, getTextureVector(i, j+1))
                    addVextexToList(textureCoords, getTextureVector(i+1, j+1))
                    addVextexToList(textureCoords, getTextureVector(i+1, j))

                    addVextexToList(normalVectors, getNormalVector(vA))
                    addVextexToList(normalVectors, getNormalVector(vB))
                    addVextexToList(normalVectors, getNormalVector(vC))
                    addVextexToList(normalVectors, getNormalVector(vD))

            self.solidArrayBufferId = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.solidArrayBufferId)
            GL.glEnableVertexAttribArray(0)
            GL.glEnableVertexAttribArray(1)
            GL.glEnableVertexAttribArray(2)
            
            idVertexBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(solidPositions)*solidPositions.itemsize, ctypes.c_void_p(solidPositions.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idTextureBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idTextureBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(textureCoords)*textureCoords.itemsize, ctypes.c_void_p(textureCoords.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(1,2,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))
        
            idNormalBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idNormalBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(normalVectors)*normalVectors.itemsize, ctypes.c_void_p(normalVectors.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(2,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

        viewPos = glm.vec3(7,3,7)
        GL.glUniform3fv(GL.glGetUniformLocation(self.pipeline, "viewPos"), 1, glm.value_ptr(viewPos))

        projection = glm.perspective(math.pi/4,self.width/self.height,0.1,100)
        camera = glm.lookAt(viewPos,glm.vec3(0,0,0),glm.vec3(0,1,0))
        model = glm.rotate(a,glm.vec3(0, 0, 1)) * glm.rotate(a/2,glm.vec3(0, 1, 0)) * glm.rotate(a/2, glm.vec3(1, 0, 0))
        mvp = projection * camera * model
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipeline, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mvp))
        
        GL.glBindVertexArray(self.solidArrayBufferId)
        GL.glDrawArrays(GL.GL_QUADS, 0, SIDES*SIDES*4)

    def draw(self):
        global a
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)

        self.drawSolid()
        a += 0.01

Solid()
