package {{ package }};

{% for import in imports %}
  import {{ import }};
{% endfor %}

import java.util.*;
import org.maluuba.service.runtime.common.Action;

{% block class_anootation %}
{% endblock %}
@JsonAutoDetect
public class {{ type }} {
  {% for fieldType, fieldRealType, fieldMeta, fieldName in fields %}
    @com.google.api.client.util.Key
    {% if 'index' in fieldMeta %}
      @Indexed
    {% endif %}
    {% if 'id' in fieldMeta %}
      @Id
    {% endif %}
    {% if 'embedded' in fieldMeta %}
      @Embedded
    {% endif %}
    public {{ fieldType }} {{ fieldName }};
  {% endfor %}

  public {{ type }}() {
  }

  public {{ type }}({{ helper.parameterList(fields) }})
    {% for fieldType, fieldRealType, fieldMeta, fieldName in fields %}
      this.{{ fieldName }} = {{ fieldName }};
    {% endfor %}
  }

  /**
   * Performs a deep copy on <i>other</i>.
   */
  public {{ type }}({{ type }} other) {
    {% for fieldType, fieldRealType, fieldMeta, fieldName in fields %}
      {% if 'primitive' in fieldMeta %}
        this.{{ fieldName }} = other.{{ fieldName }};
      {% else %}
        if (other.{{ fieldName }} != null) {
          this.{{ fieldName }} = other.{{ fieldName }}.clone();
        } else {
          this.{{ fieldName }} = null;
        }
      {% endif %}
    {% endfor %}
  }

  /**
     * Accessor for each field
     */
{% block class_accessor %}
  {% for fieldType, fieldRealType, fieldMeta, fieldName in fields %}
    public {{ fieldType }} get{{ fieldName.capitalize() }}() {
      return this.{{ fieldName }};
    }

    public {{ fieldType }} set{{ fieldName.capitalize() }}({{ fieldType }} {{ fieldName }}) {
      this.{{ fieldName }} = {{ fieldName }};
      return this;
    }
  {% endfor %}
{% endblock %}

  @Override
  public boolean equals(Object that) {
    if (that == null) {
      return false;
    }
    if (that instanceof {{ type }}) {
      return this.equals(({{ type }}) that);
    }
    return false;
  }

  public boolean equals({{ type }} that) {
    if (that == null) {
      return false;
    }

    {% for fieldType, fieldRealType, fieldMeta, fieldName in fields %}
      {% if 'primitive' in fieldMeta %}
        if (this.{{ fieldName }} != that.{{ fieldName }}) {
          return false;
        }
      {% else %}
        if (this.{{ fieldName }} != null && that.{{ fieldName }} == null) {
          return false;
        }
        if (that.{{ fieldName }} != null && this.{{ fieldName }} == null) {
          return false;
        }
        if (that.{{ fieldName }} != null && this.{{ fieldName }} != null) {
          this.{{ fieldName }}.equals(other.{{ fieldName }});
        }
      {% endif %}
    {% endfor %}
    return true;
  }

  @Override
  public String toString() {
    try {
      return new ObjectMapper().writeValueAsString(this);
    } catch (Exception e) {
      return "";
    }
  }

  public static {{ type }} valueOf(String json) {
    try {
      return new ObjectMapper().readValue(json, {{ type }}.class);
    } catch (IOException ioe) {
      return null;
    }
  }
}