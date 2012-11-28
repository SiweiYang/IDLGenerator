#!/usr/bin/env python

import unittest

from pyidl.parser import parser


class TestSetup(object):
    """PyIDL Parser test cases."""

    def setUp(self):
        pass


class TestBaseMixin(object):
    pass


class ParserTestSuite(TestSetup, TestBaseMixin, unittest.TestCase):
    def test_simple_enum(self):
        ast = parser.parse('''
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
        self.assertEquals(1, len(ast))
        enum_parse = ast[0]
        self.assertEquals('enum', enum_parse[0])
        self.assertEquals('Subgroup', enum_parse[1])
        self.assertEquals(set([
            'MUSIC_SONG_REMOVE',
            'MUSIC_SONG_INFO',
            'MUSIC_SONG_PAUSE',
            'MUSIC_RADIO',
            'MUSIC_SONG_RATING',
            'MUSIC_SONG_RESET',
            'MUSIC_SONG_RESUME',
            'MUSIC_SONG_PLAY'
            ]), set(enum_parse[2]))

    def test_simple_struct_with_namespace(self):
        ast = parser.parse('''
namespace java org.maluuba.service.MusicService

struct RequestObject {
    1: string someRequest,
    2: double someValue
}
              ''')
        self.assertEquals(2, len(ast))

        namespace_parse = ast[0]
        self.assertEquals(('namespace', 'org.maluuba.service.MusicService'), namespace_parse)

        struct_parse = ast[1]
        self.assertEquals('struct', struct_parse[0])
        self.assertEquals('RequestObject', struct_parse[1])
        self.assertEquals(('someRequest', 1, 'string'), struct_parse[2][0])
        self.assertEquals(('someValue', 2, 'double'), struct_parse[2][1])

    def test_complex_struct(self):
        ast = parser.parse('''
namespace cpp thrift.example
namespace java thrift.example

enum TweetType {
    TWEET,
    RETWEET = 2,
    DM = 0xa,
    REPLY
}

struct Location {
    1: required double latitude;
    2: required double longitude;
}

struct Tweet {
    1: required i32 userId;
    2: required string userName;
    3: required string text;
    4: optional Location loc;
    5: optional TweetType tweetType = TweetType.TWEET;
    16: optional string language = "english";
}

typedef list<Tweet> TweetList

struct TweetSearchResult {
    1: TweetList tweets;
}

const i32 MAX_RESULTS = 100;

service Twitter {
    void ping(),
    bool postTweet(1:Tweet tweet);
    TweetSearchResult searchTweets(1:string query);
    oneway void zip()
}
            ''')
        print ast
