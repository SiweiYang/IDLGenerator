package {{ package }};

import org.codehaus.jackson.map.ObjectMapper;

import javax.ws.rs.*;
import javax.ws.rs.core.*;
import javax.ws.rs.ext.*;

public class {{ type }}Reader implements MessageBodyReader<{{ type }}> {
  private final ObjectMapper m_mapper = new ObjectMapper();

  public boolean isReadable(Class<?> type, Type genericType, Annotation[] annotations, MediaType mediaType) {
    return true;
  }

  public {{ type }} readFrom(Class<{{ type }}> type,
      Type genericType, Annotation[] annotations, MediaType mediaType,
      MultivaluedMap<String, String> httpHeaders, InputStream entityStream)
    throws IOException, WebApplicationException {

    return m_mapper.readValue(entityStream, type);
  }
}