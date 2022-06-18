 #version 330 core

layout (location = 0) in vec3 vertexPos;
layout (location = 1) in vec2 vertexTexCoord;
layout (location = 2) in vec3 vertexColor;

uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;

uniform int twoDMode = 0;

out vec2 fragmentTexCoord;
out vec3 fragmentColor;

void main()
{
    if(twoDMode == 0){
        gl_Position = projection * model * view * vec4(vertexPos, 1.0);
    }else {
        gl_Position = projection * model * vec4(vertexPos, 1.0);
    }
    
    fragmentTexCoord = vertexTexCoord;
    fragmentColor = vertexColor;
}