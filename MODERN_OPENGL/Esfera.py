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

class Sphere(GLAPP):

    def setup(self):
        self.title("Esfera")
        self.size(800,800)

        GL.glClearColor(0.2, 0.2, 0.2, 0.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)

        self.pipeline = self.loadPipeline("SimplePipeline")
        GL.glUseProgram(self.pipeline)

        self.sphereArrayBufferId = None

    def drawSphere(self):
        def addVextexToList(list, vertex):
            for v in vertex:
                list.append(v)

        def getCirclePoint(i, j):
            lat = interp(i,[0,SIDES],[-math.pi/2,math.pi/2])
            lon = interp(j,[0,SIDES],[-math.pi,math.pi])
            return RADIUS*math.cos(lat)*math.sin(lon),RADIUS*math.sin(lat)*math.sin(lon),RADIUS*math.cos(lon)
            
        # def getTexturePoint(i, j):
        #     return i/SIDES, j/SIDES
        def getColorPoint(i, j):
            lat = interp(i,[0,SIDES],[-math.pi/2,math.pi/2])
            lon = interp(j,[0,SIDES],[-math.pi,math.pi])
            return math.cos(lat)*math.sin(lon), math.sin(lat)*math.sin(lon), math.cos(lon)

        if self.sphereArrayBufferId == None:
            spherePositions = array('f', [])
            colorCodes = array('f', [])

            for i in range(SIDES):           
                for j in range(SIDES):
                    addVextexToList(spherePositions, getCirclePoint(i,j))
                    addVextexToList(spherePositions, getCirclePoint(i,j+1))
                    addVextexToList(spherePositions, getCirclePoint(i+1,j+1))
                    addVextexToList(spherePositions, getCirclePoint(i+1,j))

                    addVextexToList(colorCodes, getColorPoint(i,j))
                    addVextexToList(colorCodes, getColorPoint(i,j+1))
                    addVextexToList(colorCodes, getColorPoint(i+1,j+1))
                    addVextexToList(colorCodes, getColorPoint(i+1,j))

            self.sphereArrayBufferId = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.sphereArrayBufferId)
            GL.glEnableVertexAttribArray(0)
            GL.glEnableVertexAttribArray(1)
            
            idVertexBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(spherePositions)*spherePositions.itemsize, ctypes.c_void_p(spherePositions.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idColorBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idColorBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(colorCodes)*colorCodes.itemsize, ctypes.c_void_p(colorCodes.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(1,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))
        

        projection = glm.perspective(math.pi/4,self.width/self.height,0.1,100)
        camera = glm.lookAt(glm.vec3(7,3,7),glm.vec3(0,0,0),glm.vec3(0,1,0))
        model = glm.rotate(a,glm.vec3(0, 1, 0)) * glm.rotate(a/2,glm.vec3(0, 0, 1)) * glm.rotate(a/2, glm.vec3(1, 0, 0))
        mvp = projection * camera * model
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipeline, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mvp))
        
        GL.glBindVertexArray(self.sphereArrayBufferId)
        GL.glDrawArrays(GL.GL_QUADS, 0, SIDES*SIDES*4)

    def draw(self):
        global a
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)

        self.drawSphere()
        a += 0.01

Sphere()
