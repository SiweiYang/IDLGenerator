#!/usr/bin/env python
from scanner import filterMultilineComment, filterInlineComment

__author__ = 'maluuba'
from scanner import lexer, tokens
from ply.yacc import yacc

def p_namespace(p):
  'ns : namespace java identifier'
  p[0] = (p[1], p[3])

def p_require(p):
  'req : require identifier'
  p[0] = (p[1], p[2])

def p_assignment(p):
  'assignment : identifier ASSIGN intconstant'
  p[0] = (p[1], int(p[3]))

def p_assignment_list(p):
  '''assignment_list : assignment
                     | assignment_list COMMA assignment'''
  if len(p) == 2:
    p[0] = [p[1]]
  if len(p) == 4:
    p[0] = p[1] + [p[3]]

def p_identifier_extended(p):
  '''identifier_extended : identifier
                         | Index
                         | Identifier'''
  p[0] = p[1]

def p_identifier_list(p):
  '''identifier_list : identifier
                     | identifier_list COMMA identifier'''
  if len(p) == 2:
    p[0] = [p[1]]
  if len(p) == 4:
    p[0] = p[1] + [p[3]]

def p_enum_list(p):
  '''enum_list : assignment
               | identifier
               | enum_list COMMA assignment
               | enum_list COMMA identifier'''
  if len(p) == 2:
    p[0] = [p[1]]
  if len(p) == 4:
    p[0] = p[1] + [p[3]]

def p_enum(p):
  '''enum : Enum identifier LCURLY enum_list RCURLY'''
  p[0] = ('enum', p[2], p[4])

def p_type(p):
  '''type : identifier
  | i32
  | i64
  | Boolean
  | Double
  | String
  | Object
  | Set LT type GT
  | List LT type GT
  | Map LT type COMMA type GT'''
  if len(p) == 2:
    p[0] = p[1]
  elif len(p) == 5:
    p[0] = (p[1], p[3])
  elif len(p) == 7:
    p[0] = (p[1], p[3], p[5])

def p_declaration_basic(p):
  '''declaration_basic : type identifier
                 | RangeIndex type identifier
                 | Index type identifier'''
  if len(p) == 3:
    p[0] = (p[2], None, p[1])
  if len(p) == 4:
    p[0] = (p[3], None, p[2], p[1])

def p_declaration(p):
  '''declaration : declaration_basic
                 | intconstant SEMICOLON declaration_basic'''
  if len(p) == 2:
    p[0] = p[1]
  if len(p) == 4:
    p[3] = list(p[3])
    p[3][1] = int(p[1])
    p[0] = tuple(p[3])

def p_declaration_list(p):
  '''declaration_list : declaration
                      | declaration_list COMMA declaration'''
  if len(p) == 2:
    p[0] = [p[1]]
  if len(p) == 4:
    p[0] = p[1] + [p[3]]

def p_struct_annotation(p):
  '''struct_annotation : Struct identifier'''
  p[0] = (p[2])

def p_struct_annotation_response(p):
  '''struct_annotation : Struct identifier Response'''
  p[0] = (p[2], 'response')

def p_struct_annotation_persistent(p):
  '''struct_annotation : Struct identifier Persistent
                       | Struct identifier Persistent LPAREN identifier RPAREN
                       | Struct identifier Persistent LPAREN identifier COMMA identifier RPAREN'''
  if len(p) == 4:
    p[0] = (p[2], 'persistent', 'dynamo', p[2])
  if len(p) == 7:
    p[0] = (p[2], 'persistent', 'dynamo', p[5])
  if len(p) == 9:
    p[0] = (p[2], 'persistent', p[7], p[5])

def p_struct_basic(p):
  '''struct : struct_annotation LCURLY RCURLY
            | struct_annotation LCURLY declaration_list RCURLY'''
  if len(p) == 4:
    p[0] = ('struct', p[1], [])
  if len(p) == 5:
    p[0] = ('struct', p[1], p[3])

def p_function_basic(p):
  '''function_basic : type identifier_extended LPAREN RPAREN
                    | type identifier_extended LPAREN declaration_list RPAREN'''
  if len(p) == 5:
    p[0] = (p[2], p[1], [])
  if len(p) == 6:
    p[0] = (p[2], p[1], p[4])

def p_function_post(p):
  '''function : Post function_basic
              | function_basic'''
  if len(p) == 2:
    p[0] = p[1]
  if len(p) == 3:
    p[0] = p[2]

def p_function_list(p):
  '''function_list : function_list function COMMA
                   | function_list function COLON
                   | function_list function
                   | function COMMA
                   | function COLON
                   | function'''
  if len(p) == 2:
    p[0] = [p[1]]
  if len(p) == 3:
    if p[2] == ',':
      p[0] = [p[1]]
    elif p[2] == ';':
      p[0] = [p[1]]
    else:
      p[0] = p[1] + [p[2]]
  if len(p) == 4:
    p[0] = p[1] + [p[2]]

def p_service(p):
  'service : Service identifier LCURLY function_list RCURLY'
  p[0] = ('service', p[2], p[4])

def p_document(p):
  '''document : ns
              | req
              | enum
              | struct
              | service
              | document document'''
  if len(p) == 2:
    p[0] = [p[1]]
  if len(p) == 3:
    p[0] = p[1] + p[2]

def p_error(t):
  print("Syntax error at '%s'" % t.value)

start = 'document'
parser = yacc()

def parse(str):
  str = filterMultilineComment(str)
  str = filterInlineComment(str)
  #print str
  return parser.parse(str)

if __name__ == '__main__':
  ast = parse('''
  namespace java org.maluuba.service.MusicService

  struct RequestObject {
    1: string someRequest,
    2: double someValue
  }
  ''')

  for item in ast:
    print item

  ast = parse('''
  enum Subgroup {
    MUSIC_SONG_REMOVE,
    MUSIC_SONG_INFO,
    MUSIC_SONG_PAUSE,
    MUSIC_RADIO,
    MUSIC_SONG_RATING,
    MUSIC_SONG_RESET,
    MUSIC_SONG_RESUME,
    MUSIC_SONG_PLAY
  }
  ''')

  for item in ast:
    print item

  ast = parse('''
namespace java org.maluuba.service.timeline

enum EventType {
  ALL = 0,
  CALL = 1,
  ALARM = 2,
  CALENDAR = 3,
	REMINDERS = 4
}

struct Gps{
	1: double lat,
	2: double lon
}

struct CalendarContact{
	1: string name,
	2: string email,
    3: string contactKey,
	4: string phoneKey
}

struct UserEvent persistent(UserEvents) {
  1: index string userId,
  2: range-index i64 triggerTime,
  3: string eventId,
  4: EventType type,
  5: i64 createdAt
}

struct CallEvent persistent(CallEvents) {
  1: index string eventId,
  2: string phoneNumber
}

struct TimeTriggeredEvent persistent(TimeTriggeredEvents) {
  1: index string eventId,
  2: range-index i64 triggerTime,
  3: EventType type,
  4: string eventAction
}

struct AlarmTimeTriggeredEvent persistent(AlarmTimeTriggeredEvents) {
  1: index string eventId,
  2: string alarmMessage,
  3: i64 triggerTime
}

struct CalendarTimeTriggeredEvent persistent(CalendarTimeTriggeredEvents) {
  1: index string eventId,
  2: set<CalendarContact> contacts,
  3: i64 date,
  4: i64 duration,
  5: string location,
  6: string meetingTitle,
  7: set<string> repeatDays,
  8: i64 repeatDaysLength,
  9: string googleId
}

struct ReminderTimeTriggeredEvent persistent(ReminderTimeTriggeredEvents) {
  1: index string eventId,
  2: string ReminderMessage,
  3: i64 triggerTime
}

struct RemindersLocationTriggeredEvent persistent(RemindersLocationTriggeredEvents) {
  1: index string eventId,
  2: string remindersMessage,
	3: string location,
	4: Gps locationGps,
	5: bool toFlag //To or From Location
}


struct GetTimelineEventRequest {
  1: string userId,
  2: string eventId
}

struct GetTimelineEventResponse {
  1: UserEvent event
}

struct GetTimelineRequest {
  1: string userId,
  2: EventType type,
  3: i64 from,
  4: i64 to
}

struct GetTimelineResponse {
  1: list<UserEvent> events,
  2: i64 lastModifiedAt,
  3: bool forceOverwrite
}

struct GetTimeTriggeredEventsRequest {
  1: string userId,
  2: i64 from,
  3: i64 to
}

struct GetTimeTriggeredEventsResponse {
  1: list<TimeTriggeredEvent> events,
  2: bool forceOverwrite
}

//Get Multiple events
struct GetCalendarTimeTriggeredEventsRequest {
  1: string userId,
  2: i64 from,
  3: i64 to
}

struct GetCalendarTimeTriggeredEventsResponse {
  1: list<CalendarTimeTriggeredEvent> events,
  2: bool forceOverwrite,
  3: i64 lastModifiedAt
}

struct GetAlarmTimeTriggeredEventsRequest {
  1: string userId,
  2: i64 from,
  3: i64 to
}

struct GetAlarmTimeTriggeredEventsResponse {
  1: list<AlarmTimeTriggeredEvent> events,
  2: bool forceOverwrite,
  3: i64 lastModifiedAt
}

struct GetReminderTimeTriggeredEventsRequest {
  1: string userId,
  2: i64 from,
  3: i64 to
}

struct GetReminderTimeTriggeredEventsResponse {
  1: list<ReminderTimeTriggeredEvent> events,
  2: bool forceOverwrite,
  3: i64 lastModifiedAt
}

//Get Single Events

struct GetEventRequest {
  1: string userId,
  2: string eventId
}

struct GetAlarmTimeTriggeredEventResponse {
  1: AlarmTimeTriggeredEvent event,
  2: i64 lastModifiedAt
}

struct GetCalendarTimeTriggeredEventResponse {
  1: CalendarTimeTriggeredEvent event,
  2: i64 lastModifiedAt
}

struct GetReminderTimeTriggeredEventResponse {
  1: ReminderTimeTriggeredEvent event,
  2: i64 lastModifiedAt
}

struct PutCallEventRequest {
  1: UserEvent userEvent,
  2: CallEvent callEvent
}

struct PutCallEventResponse {
  1: string eventId
}

struct PutAlarmTimeTriggeredEventRequest {
  1: UserEvent userEvent,
  2: TimeTriggeredEvent timeTriggeredEvent,
  3: AlarmTimeTriggeredEvent alarmTimeTriggeredEvent
}

struct PutAlarmTimeTriggeredEventResponse {
  1: string eventId
}

struct PutCalendarTimeTriggeredEventRequest {
  1: UserEvent userEvent,
  2: TimeTriggeredEvent timeTriggeredEvent,
  3: CalendarTimeTriggeredEvent calendarTimeTriggeredEvent,
  4: string authTotken
}

struct PutCalendarTimeTriggeredEventResponse {
  1: string eventId,
  2: i64 oldTimestamp,
  3: i64 timestamp
}

struct ModifyCalendarEventRequest {
  1: set<string> addContacts,
  2: set<string> deleteContacts,
  3: string replacementTitle,
  4: i64 replacementTime,
  5: i64 replacementDate,
  6: string replacementLocation,
  7: i64 replacementDuration,
  8: string userId,
  9: string eventId,
  10: string authToken
}

struct ModifyCalendarEventResponse {
  1: i64 oldTimestamp,
  2: i64 timestamp
}


struct RemoveEventRequest {
  1: string userId,
  2: string eventId
}

struct RemoveEventResponse {
  1: i64 oldTimestamp,
  2: i64 timestamp
}

struct PutReminderTimeTriggeredEventRequest {
  1: UserEvent userEvent,
  2: TimeTriggeredEvent timeTriggeredEvent,
  3: ReminderTimeTriggeredEvent ReminderTimeTriggeredEvent
}

struct PutReminderTimeTriggeredEventResponse {
  1: string eventId
}


struct LastModifiedResponse {
  1: i64 timestamp
}

struct LastModifiedRequest {
  1: string userId
}

struct GoogleCalendarEvent persistent(GoogleCalendarEvents) {
  1: index string googleId,
  2: string eventId,
  3: i64 timestamp
}

struct UserGoogleCalendar persistent(UserGoogleCalendars) {
  1: index string userId,
  2: string calendarId,
  3: i64 timestamp,
  4: string authToken,
  5: string refreshToken
}

struct GoogleEvent {
  1: string meetingTitle,
  2: i64 triggerTime,
  3: string id
}

struct GetEventsRequest {
  1: string userId,
  2: string calendarName
}

struct GetEventsResponse {
  1: list<GoogleEvent> events,
  2: string reserved
}

struct SyncResponse {
  1: list<CalendarTimeTriggeredEvent> events,
  2: list<string> removedEvents,
  3: i64 oldTimestamp,
  4: i64 timestamp
}

struct SyncRequest {
  1: i64 startTime,
  2: i64 endTIme,
  3: string authToken,
  4: string userId
}

service Timeline {
  GetTimelineResponse getTimeline(1: GetTimelineRequest request);

  GetTimeTriggeredEventsResponse getTimeTriggeredEvents(1: GetTimeTriggeredEventsRequest request);

  GetCalendarTimeTriggeredEventsResponse getCalendarTimeTriggeredEvents(1: GetCalendarTimeTriggeredEventsRequest request);
  GetReminderTimeTriggeredEventsResponse getReminderTimeTriggeredEvents(1: GetReminderTimeTriggeredEventsRequest request);
  GetAlarmTimeTriggeredEventsResponse getAlarmTimeTriggeredEvents(1: GetAlarmTimeTriggeredEventsRequest request);

  GetCalendarTimeTriggeredEventResponse getCalendarTimeTriggeredEvent(1: GetEventRequest request);
  GetReminderTimeTriggeredEventResponse getReminderTimeTriggeredEvent(1: GetEventRequest request);
  GetAlarmTimeTriggeredEventResponse getAlarmTimeTriggeredEvent(1: GetEventRequest request);


  PutCallEventResponse putCallEvent(1: PutCallEventRequest request);
  PutAlarmTimeTriggeredEventResponse putAlarmTimeTriggeredEvent(1: PutAlarmTimeTriggeredEventRequest request);
  PutCalendarTimeTriggeredEventResponse putCalendarTimeTriggeredEvent(1: PutCalendarTimeTriggeredEventRequest request);

  PutReminderTimeTriggeredEventResponse putReminderTimeTriggeredEvent(1: PutReminderTimeTriggeredEventRequest request);

  SyncResponse  SyncCalendar(1: SyncRequest request)
  GetEventsResponse getCalendarEvents(1: GetEventsRequest request)


  ModifyCalendarEventResponse modifyCalendarTimeTriggeredEvent(1: ModifyCalendarEventRequest request);
  RemoveEventResponse removeEvent(1: RemoveEventRequest request);

  LastModifiedResponse getLastModified(1: LastModifiedRequest request);
}
  ''')

  for item in ast:
    print item