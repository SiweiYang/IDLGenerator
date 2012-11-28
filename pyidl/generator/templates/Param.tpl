package {{ package }};

import java.util.List;
import java.util.Map;
import java.util.Set;

import org.codehaus.jackson.map.ObjectMapper;
import org.maluuba.service.runtime.common.RequestInfo;
import org.codehaus.jackson.annotate.JsonAutoDetect;

@JsonAutoDetect
public class {{ type.capitalize() }}Params {

  {% for fieldType, fieldRealType, fieldMeta, fieldName in fields %}
    @org.codehaus.jackson.annotate.JsonProperty
    public {{ fieldType }} {{ fieldName }};
  {% endfor %}
  @org.codehaus.jackson.annotate.JsonProperty
  public RequestInfo requestInfo;
  @org.codehaus.jackson.annotate.JsonProperty
  public String oauthToken;

  @Override
  public String toString() {
    try {
      return new ObjectMapper().writeValueAsString(this);
    } catch (Exception e) {
      return "";
    }
  }

  public {{ type.capitalize() }}Url toUrl(String url) {
    {{ type.capitalize() }}Url url_ = new {{ type.capitalize() }}Url(url);
    {% for fieldType, fieldRealType, fieldMeta, fieldName in fields %}
      url_.{{ fieldName }} = this.{{ fieldName }};
    {% endfor %}
    url_.requestInfo = this.requestInfo;
    url_.oauthToken = this.oauthToken;

    return url_;
  }
}