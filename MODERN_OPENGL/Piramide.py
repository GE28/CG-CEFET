from GLAPP import GLAPP
from OpenGL import GL
from array import array
import ctypes
import glm
import math
a = 0
b = 3
PIECES = 7
STEP = 0.02

class PyramidWithTextureApp(GLAPP):

    def setup(self):
        self.title("Piramide")
        self.size(800,800)

        GL.glClearColor(0.2, 0.2, 0.2, 0.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)

        self.pipeline = self.loadPipeline("SimpleTexture")
        GL.glUseProgram(self.pipeline)

        GL.glActiveTexture(GL.GL_TEXTURE0)
        self.loadTexture("./textures/uv_grid_opengl.png")
        GL.glUniform1i(GL.glGetUniformLocation(self.pipeline, "textureSlot"),0)

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

            textureCoord = array('f',[
                1,0,
                0,0,
                0.5, 0.5,

                0,1,
                1,1,
                0.5, 0.5,

                1,0,
            ])

            self.pyramidArrayBufferId = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.pyramidArrayBufferId)
            GL.glEnableVertexAttribArray(0)
            GL.glEnableVertexAttribArray(1)
            
            idVertexBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(position)*position.itemsize, ctypes.c_void_p(position.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idTextureBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idTextureBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(textureCoord)*textureCoord.itemsize, ctypes.c_void_p(textureCoord.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(1,2,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))
        

        projection = glm.perspective(math.pi/4,self.width/self.height,0.1,100)
        camera = glm.lookAt(glm.vec3(4,1,4),glm.vec3(0,0,0),glm.vec3(0,1,0))
        model = glm.rotate(a,glm.vec3(0, 1, 0)) * glm.rotate(0.04, glm.vec3(1, 1, 1))
        mvp = projection * camera * model
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipeline, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mvp))
        GL.glBindVertexArray(self.pyramidArrayBufferId)
        GL.glDrawArrays(GL.GL_TRIANGLE_STRIP,0,math.floor(b) if b <= PIECES + 10 * STEP else PIECES)

    def draw(self):
        global a, b
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)

        self.drawPyramid()
        if b >= (PIECES + 10):
            b = 0
        a += 0.01
        b += STEP

PyramidWithTextureApp()
