#version 400

in vec2 textureCoord;
uniform sampler2D textureSlot;
out vec4 color;

void main(void) 
{
    color = texture(textureSlot,textureCoord);
}
