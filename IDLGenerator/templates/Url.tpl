package {{ package }};

import java.util.List;
import java.util.Map;
import java.util.Set;

import com.google.api.client.http.GenericUrl;
import org.maluuba.service.runtime.SerializedObject;
import org.maluuba.service.runtime.common.RequestInfo;



public class {{ type.capitalize() }}Url extends GenericUrl {
  public {{ type.capitalize() }}Url(String encodedUrl) {
    super(encodedUrl);
  }

  {% for fieldType, fieldRealType, fieldMeta, fieldName in fields %}
      @com.google.api.client.util.Key
      public {{ fieldType }} {{ fieldType }};
  {% endfor %}

  @com.google.api.client.util.Key
  public RequestInfo requestInfo;
}