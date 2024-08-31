#!/bin/bash
say() { local IFS=+; cvlc -q --play-and-exit "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=ms"; }
say $*
