#version 430

uniform mat4 p3d_ViewMatrix;

in vertex_data {
    vec2 uv;
    vec3 normal;
    vec3 FragPos;
    vec3 lightPos;
} data;

struct Material{
    vec4 color;
    vec3 specular;
    vec3 diffuse;
    sampler2D texture;
    sampler2D specular_map;
    int shininess;
    vec2 texture_scale;
};

uniform Material material;

struct Light{
    vec3 direction;
    float innerCutOff;
    float outerCutOff;
    vec3 diffuse;
    vec3 ambient;
    vec3 specular;
    bool on;

};

uniform Light light;


out vec4 color;

void main() {

    vec3 lightDir = normalize(data.lightPos - data.FragPos);
    vec3 lDir = -normalize(vec3(mat3(p3d_ViewMatrix) * light.direction));
    float theta = dot(lightDir, normalize(lDir));
    float epsilon   = light.innerCutOff - light.outerCutOff;
    float intensity = clamp((theta - light.outerCutOff) / epsilon, 0.0, 1.0);

    vec2 scaled_uv = data.uv * material.texture_scale;

    vec4 texColor = texture(material.texture, scaled_uv);
    vec4 specColor = texture(material.specular_map, scaled_uv);

    vec3 ambient = light.ambient * texColor.rgb;
    vec3 diffuse = light.diffuse * material.diffuse * max(dot(normalize(data.normal), lightDir), 0.0) * texColor.rgb;
    vec3 viewDir = normalize(- data.FragPos);
    vec3 reflectDir = reflect(-lightDir, normalize(data.normal));
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    vec3 specular = light.specular * material.specular * spec * specColor.rgb;

    ambient *= intensity;
    diffuse *= intensity;
    specular *= intensity;

    vec3 result = ambient + diffuse + specular;

    color = vec4(result, texColor.a);
}