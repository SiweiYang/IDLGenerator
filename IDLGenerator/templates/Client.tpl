{$preamble}

package {$package};

{% for import in imports %}
    import {$import};
{% endfor %}

import org.codehaus.jackson.JsonNode;
import com.google.api.client.http.json.JsonHttpContent;
import org.maluuba.service.runtime.common.exceptions.MaluubaException;
import org.maluuba.service.runtime.common.exceptions.NetworkException;
import org.maluuba.service.runtime.common.MaluubaResponse;
import org.maluuba.service.runtime.common.PlatformResponse;
import org.maluuba.service.runtime.common.RequestInfo;
import org.maluuba.service.runtime.EnvironmentType;

public class {$clientName} implements {$interfaceName} {
  static final HttpTransport HTTP_TRANSPORT = new NetHttpTransport();
  static final JsonFactory JSON_FACTORY = new JacksonFactory();

  private String serviceHost = "http://{$service_id}.%s.service.maluuba.com";
  private EnvironmentType environment = EnvironmentType.DEV;

  /**
  * Returns the base host name the client uses to make calls.
  *
  * By default, this host name is the ELB that the service is deployed to.
  */
  public String getServiceHost() {
    return String.format(serviceHost, environment.getUrlComponent());
  }

  /**
  * Sets the base host name the client uses to make calls.
  *
  * This is mostly only useful for debugging purposes. The default host name
  * should be correct in the majority of cases.
  */
  public void setServiceHost(String serviceHost) {
    this.serviceHost = serviceHost;
  }

  public EnvironmentType getEnvironment() {
    return environment;
  }

  public void setEnvironment(EnvironmentType environment) {
    this.environment = environment;
  }

  {% for operation in operations %}
    {% if operation.method == "@POST" %}
        class {$operation.type_name}PostParams {
            {% for param in operation.params %}
                @com.google.api.client.util.Key public {$param.type} {$param.name};
            {% endfor %}
            @com.google.api.client.util.Key public RequestInfo requestInfo;
        }
    {% endif %}
  {% endfor %}

  {% for operation in operations %}
    {$operation.javadoc}
    {% if operation.is_maluuba_response == "true" %}
        public MaluubaResponse {$operation.name}({% for param in operation.params %}{$param.type} {$param.name}, {% endfor %} RequestInfo requestInfo) throws MaluubaException {
    {% endif %}

    {% if operation.is_maluuba_response == "false" %}
    public {$operation.return_type} {$operation.name}({% for param in operation.params %}{$param.type} {$param.name}, {% endfor %} RequestInfo requestInfo) throws MaluubaException {
    {% endif %}

       HttpRequestFactory requestFactory = HTTP_TRANSPORT.createRequestFactory(new HttpRequestInitializer() {
        @Override
        public void initialize(HttpRequest request) {
            request.addParser(new JsonHttpParser(JSON_FACTORY));
        }
       });

        {$operation.type_name}Url url_ = new {$operation.type_name}Url(String.format("%s/service/%s", getServiceHost(), "{$operation.name}"));
        {% if operation.method == "@GET" %}
            url_.requestInfo = requestInfo;
            {% for param in operation.params %}
                url_.{$param.name} = {$param.name};
            {% endfor %}
        {% elif operation.method == "@POST" %}
            {$operation.type_name}PostParams params_ = new {$operation.type_name}PostParams();
            params_.requestInfo = requestInfo;
            {% for param in operation.params %}
                params_.{$param.name} = {$param.name};
            {% endfor %}
        {% endif %}

        try {
            {% if operation.method == "@GET" %}
            HttpRequest request_ = requestFactory.buildGetRequest(url_);
            {% endif %}
            {% if operation.method == "@POST" %}
            HttpRequest request_ = requestFactory.buildPostRequest(url_, new JsonHttpContent(JSON_FACTORY, params_));
            {% endif %}
            String strResponse = request_.execute().parseAsString();
            {% if operation.is_maluuba_response == "true" %}
            JsonNode jsonResponse = new ObjectMapper().readValue(strResponse, JsonNode.class);
            MaluubaResponse response_ = new ObjectMapper().readValue(strResponse, MaluubaResponse.class);
            if (jsonResponse.has("platformResponse") && !jsonResponse.get("platformResponse").isNull()) {
            response_.getPlatformResponse().setJsonText(jsonResponse.get("platformResponse").toString());
            }
            if (jsonResponse.has("exception") && !jsonResponse.get("exception").isNull()) {
            response_.getException().setJsonText(jsonResponse.get("exception").toString());
            }
            {% endif %}
            {% if operation.is_maluuba_response == "false" %}
            {$operation.return_type} response_ = new ObjectMapper().readValue(strResponse, {$operation.return_type}.class);
            {% endif %}
            return response_;
        } catch (IOException ioe) {
            throw new NetworkException(requestInfo, "Network exception communicating with server", ioe);
        }
      }
  {% endfor %}
}