package {$package};

{% for import in imports %}
  import {$import};
{% endfor %}

import java.util.*;
import org.maluuba.service.runtime.common.Action;

{% if persistent %}
  {% if persistent[1] == 'dynamo' %}
    import com.amazonaws.services.dynamodb.datamodeling.DynamoDBTable;
    import com.amazonaws.services.dynamodb.datamodeling.DynamoDBAttribute;
    import com.amazonaws.services.dynamodb.datamodeling.DynamoDBHashKey;
    import com.amazonaws.services.dynamodb.datamodeling.DynamoDBRangeKey;

    @DynamoDBTable(tableName="{{ persistent[0] }}")
  {% elif persistent[1] == 'mongo' %}
    import com.google.code.morphia.annotations.Entity;
    import com.google.code.morphia.annotations.Embedded;
    import com.google.code.morphia.annotations.Id;
    import com.google.code.morphia.annotations.Indexed;
    import com.google.code.morphia.annotations.Property;

    @Entity(value="{{ persistent[0] }}", noClassnameStored=true)
  {% if endif %}
{% endif %}

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

  public {{ type }}({{helper.parameterList(fields)}})
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
  {% for field in fields %}
    {% if persistent == "true" %}
      {% if provider == "dynamo" %}
        {% if field.hash_index == "true" %}
          @DynamoDBHashKey(attributeName="{$field.name}")
        {% endif %}
        {% if field.range_index == "true" %}
          @DynamoDBRangeKey(attributeName="{$field.name}")
        {% endif %}
        {% if field.no_index == "true" %}
          @DynamoDBAttribute(attributeName="{$field.name}")
        {% endif %}
      {% endif %}
    {% endif %}
    
    {% if persistent == "true" %}
      {% if provider == "mongo" %}
        {% if field.id_index == "true" %}
          @JsonProperty("_id")
        {% endif %}
        {% if field.id_index == "false" %}
          @JsonProperty("{$field.name}")
        {% endif %}
      {% endif %}
    {% endif %}
    public {$field.type} get{$field.capitalized_name}() {
      return this.{$field.name};
    }
  
    {% if persistent == "true" %}
      {% if provider == "mongo" %}
        {% if field.id_index == "true" %}
          @JsonProperty("_id")
        {% endif %}
        {% if field.id_index == "false" %}
          @JsonProperty("{$field.name}")
        {% endif %}
      {% endif %}
    {% endif %}
    public {$dataTypeName} set{$field.capitalized_name}({$field.type} {$field.name}) {
      this.{$field.name} = {$field.name};
      return this;
    }
  {% endfor %}

  @Override
  public boolean equals(Object that) {
    if (that == null) {
      return false;
    }
    if (that instanceof {$dataTypeName}) {
      return this.equals(({$dataTypeName}) that);
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