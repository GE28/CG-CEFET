from GLAPP import GLAPP
from OpenGL import GL
from array import array
import ctypes
import glm
import math
from random import uniform
a = 0
STEP = 0.01

class PyramidWithTextureApp(GLAPP):

    def setup(self):
        self.title("Piramide")
        self.size(800,800)

        GL.glClearColor(0.2, 0.2, 0.2, 0.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)

        self.pipeline = self.loadPipeline("SimpleLightning")
        GL.glUseProgram(self.pipeline)

        self.pyramidArrayBufferId = None

    def drawPyramid(self):
        if self.pyramidArrayBufferId == None:
            position = array('f',[
                -1.0, -1.0, 1.0,      #a     
                 1.0, -1.0, 1.0,      #b      
                 0.0,  1.0, 0.0,      #e    

                 1.0, -1.0, -1.0,     #c
                -1.0, -1.0, -1.0,     #d
                 0.0,  1.0, 0.0,      #e  

                -1.0, -1.0, 1.0,      #a       
            ])

            colorVecs = array('f',[
                1, 0, 0, #a
                0, 1, 0, #b
                0, 0, 1, #e

                1, 0, 0, #c
                0, 1, 0, #d
                0, 0, 1, #e

                1, 0, 0, #a
            ])

            normalVectors = array('f',[
                -0.5, -0.5, 0.5, #a
                0.5, -0.5, 0.5, #b
                0.0, 0.5, 0.0, #e

                0.5, -0.5, -0.5, #c
                -0.5, -0.5, -0.5, #d
                0.0, 0.5, 0.0, #e

                -0.5, -0.5, 0.5, #a
            ])

            self.pyramidArrayBufferId = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.pyramidArrayBufferId)
            GL.glEnableVertexAttribArray(0)
            GL.glEnableVertexAttribArray(1)
            GL.glEnableVertexAttribArray(2)
            
            idVertexBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(position)*position.itemsize, ctypes.c_void_p(position.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idColorBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idColorBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(colorVecs)*colorVecs.itemsize, ctypes.c_void_p(colorVecs.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(1,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idNormalBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idNormalBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(normalVectors)*normalVectors.itemsize, ctypes.c_void_p(normalVectors.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(2,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))
        

        viewPos = glm.vec3(4,1,4)
        GL.glUniform3fv(GL.glGetUniformLocation(self.pipeline, "viewPos"), 1, glm.value_ptr(viewPos))

        lightPosition = glm.rotate(a,glm.vec3(0, 1, 0)) * glm.rotate(a/2,glm.vec3(1, 0, 0)) * glm.vec3(10.0,5.0,5.0)
        GL.glUniform3fv(GL.glGetUniformLocation(self.pipeline, "lightPosition"), 1, glm.value_ptr(lightPosition))

        projection = glm.perspective(math.pi/4,self.width/self.height,0.1,100)
        camera = glm.lookAt(viewPos, glm.vec3(0,0,0), glm.vec3(0,1,0))
        model = glm.rotate(a,glm.vec3(0, 1, 0))
        mvp = projection * camera * model
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipeline, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mvp))

        GL.glBindVertexArray(self.pyramidArrayBufferId)
        GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, 0, 7)

    def draw(self):
        global a, b
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)

        self.drawPyramid()
        a += 0.01

PyramidWithTextureApp()
