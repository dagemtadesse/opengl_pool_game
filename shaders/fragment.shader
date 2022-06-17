#version 330 core
 
in vec2 fragmentTexCoord;
in vec3 fragmentColor;

out vec4 outColor;

uniform sampler2D imageTexture;
uniform int twoDMode = 0;

void main()
{
    if(twoDMode == 0){
        outColor = texture(imageTexture, fragmentTexCoord);
    }else {
        outColor = vec4(fragmentColor, 1.0);
    }
}