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

        self.pipeline = self.loadPipeline("SimpleTexture")
        GL.glUseProgram(self.pipeline)

        GL.glActiveTexture(GL.GL_TEXTURE0)
        self.loadTexture("./textures/uv_grid_opengl.png")
        GL.glUniform1i(GL.glGetUniformLocation(self.pipeline, "textureSlot"),0)

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

        def getNormalVector(v,i,j):
            parc1 = getCirclePoint(i,j+0.1)
            parc2 = getCirclePoint(i+0.1,j)
            v1 = glm.vec3(parc1[0]-v[0],parc1[1]-v[1],parc1[2]-v[2])
            v2 = glm.vec3(parc2[0]-v[0],parc2[1]-v[1],parc2[2]-v[2])
            n = glm.normalize(glm.cross(v1,v2))
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

                    addVextexToList(normalVectors, getNormalVector(vA, i, j))
                    addVextexToList(normalVectors, getNormalVector(vB, i, j+1))
                    addVextexToList(normalVectors, getNormalVector(vC, i+1, j+1))
                    addVextexToList(normalVectors, getNormalVector(vD, i+1, j))

            self.solidArrayBufferId = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.solidArrayBufferId)
            GL.glEnableVertexAttribArray(0)
            GL.glEnableVertexAttribArray(1)
            
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

        projection = glm.perspective(math.pi/4,self.width/self.height,0.1,100)
        camera = glm.lookAt(glm.vec3(7,3,7),glm.vec3(0,0,0),glm.vec3(0,1,0))
        model = glm.rotate(a,glm.vec3(0, 1, 0)) * glm.rotate(a/2,glm.vec3(0, 0, 1)) * glm.rotate(a/2, glm.vec3(1, 0, 0))
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
