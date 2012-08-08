{% extends 'Object.tpl' %}

{% block class_anootation %}
import com.amazonaws.services.dynamodb.datamodeling.DynamoDBTable;
import com.amazonaws.services.dynamodb.datamodeling.DynamoDBAttribute;
import com.amazonaws.services.dynamodb.datamodeling.DynamoDBHashKey;
import com.amazonaws.services.dynamodb.datamodeling.DynamoDBRangeKey;

@DynamoDBTable(tableName="{{ persistent[0] }}")
{% endblock %}

{% block class_accessor %}
  {% for fieldType, fieldRealType, fieldMeta, fieldName in fields %}
    {% if 'index' in fieldMeta %}
      @DynamoDBHashKey(attributeName="{{ fieldName }}")
    {% elif 'range' in fieldMeta %}
      @DynamoDBRangeKey(attributeName="{{ fieldName }}")
    {% else %}
      @DynamoDBAttribute(attributeName="{{ fieldName }}")
    {% endif %}
    public {{ fieldType }} get{{ fieldName.capitalize() }}() {
      return this.{{ fieldName }};
    }

    public {{ fieldType }} set{{ fieldName.capitalize() }}({{ fieldType }} {{ fieldName }}) {
      this.{{ fieldName }} = {{ fieldName }};
      return this;
    }
  {% endfor %}
{% endblock %}