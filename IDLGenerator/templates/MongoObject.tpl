{% extends 'Object.tpl' %}

{% block class_anootation %}
import com.google.code.morphia.annotations.Entity;
import com.google.code.morphia.annotations.Embedded;
import com.google.code.morphia.annotations.Id;
import com.google.code.morphia.annotations.Indexed;
import com.google.code.morphia.annotations.Property;

@Entity(value="{{ persistent[0] }}", noClassnameStored=true)
{% endblock %}

{% block class_accessor %}
  {% for fieldType, fieldRealType, fieldMeta, fieldName in fields %}
    {% if 'id' in fieldMeta %}
      @JsonProperty("_id")
    {% else %}
      @JsonProperty("{{ fieldName }}")
    {% endif %}

    public {{ fieldType }} get{{ fieldName.capitalize() }}() {
      return this.{{ fieldName }};
    }

    {% if 'id' in fieldMeta %}
      @JsonProperty("_id")
    {% else %}
      @JsonProperty("{{ fieldName }}")
    {% endif %}
    public {{ fieldType }} set{{ fieldName.capitalize() }}({{ fieldType }} {{ fieldName }}) {
      this.{{ fieldName }} = {{ fieldName }};
      return this;
    }
  {% endfor %}
{% endblock %}