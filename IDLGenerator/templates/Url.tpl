package {$package};

import java.util.List;
import java.util.Map;
import java.util.Set;

import com.google.api.client.http.GenericUrl;
import org.maluuba.service.runtime.SerializedObject;
import org.maluuba.service.runtime.common.RequestInfo;



public class {$capitalized_name}Url extends GenericUrl {
  public {$capitalized_name}Url(String encodedUrl) {
    super(encodedUrl);
  }

  {% for param in params %}
      @com.google.api.client.util.Key
      public {$param.type} {$param.name};
  {% endfor %}

  @com.google.api.client.util.Key
  public RequestInfo requestInfo;
}