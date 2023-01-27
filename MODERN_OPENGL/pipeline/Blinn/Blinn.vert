// from: https://learnopengl.com/Advanced-Lighting/Advanced-Lighting
// code: https://learnopengl.com/code_viewer_gh.php?code=src/5.advanced_lighting/1.advanced_lighting/1.advanced_lighting.vs
#version 400

layout (location=0) in vec3 attr_position;
layout (location=1) in vec2 attr_textureCoord;
layout (location=2) in vec3 attr_normal;

uniform mat4 MVP;
out vec3 fragPos;
out vec2 textureCoord;
out vec3 normalPos;

void main(void) 
{
    textureCoord = attr_textureCoord;
    gl_Position = MVP * vec4(attr_position,1.0);
    fragPos = attr_position;
    normalPos = attr_normal;
}