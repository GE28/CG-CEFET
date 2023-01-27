// from: https://learnopengl.com/Advanced-Lighting/Advanced-Lighting
// code: https://learnopengl.com/code_viewer_gh.php?code=src/5.advanced_lighting/1.advanced_lighting/1.advanced_lighting.fs
#version 400

in vec3 fragPos;
in vec3 colorVec;
in vec3 normalPos;

uniform vec3 lightPosition;
uniform vec3 viewPos;
out vec4 color;

void main(void) 
{   
    vec3 iColor = colorVec;

    vec3 ambient = 0.05 * iColor;

    vec3 lightDir = normalize(lightPosition - fragPos);
    vec3 normal = normalize(normalPos);
    float diff = max(dot(lightDir, normal), 0.0);
    vec3 diffuse = diff * iColor;

    vec3 viewDir = normalize(viewPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = 0.0;
    
    vec3 halfwayDir = normalize(lightDir + viewDir);  
    spec = pow(max(dot(normal, halfwayDir), 0.0), 32.0);

    vec3 specular = vec3(0.3) * spec; 
    color = vec4(ambient + diffuse + specular, 1.0);
}