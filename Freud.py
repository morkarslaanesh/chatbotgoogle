# coding=UTF-8
# Natural Language Toolkit: Eliza
#
# Copyright (C) 2001-2013 NLTK Project
# Authors: Steven Bird <stevenbird1@gmail.com>
#          Edward Loper <edloper@gmail.com>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

# Based on an Eliza implementation by Joe Strout <joe@strout.net>,
# Jeff Epler <jepler@inetnebr.com> and Jez Higgins <mailto:jez@jezuk.co.uk>.

# a translation table used to convert things you say into things the
# computer says back, e.g. "I am" --> "you are"
# from __future__ import print_function
# from nltk.chat import Chat
from util import *


reflections = {
  "i am"       : "you are",
  "i was"      : "you were",
  "i"          : "you",
  "i'm"        : "you are",
  "i'd"        : "you would",
  "i've"       : "you have",
  "i'll"       : "you will",
  "my"         : "your",
  "you are"    : "I am",
  "you were"   : "I was",
  "you've"     : "I have",
  "you'll"     : "I will",
  "your"       : "my",
  "yours"      : "mine",
  "you"        : "me",
  "me"         : "you"
}

# a table of response pairs, where each pair consists of a
# regular expression, and a list of possible responses,
# with group-macros labelled as %1, %2.

pairs = (
  (r'I need (.*)',
  ( "Why do you need %1?",
    "Would it really help you to get %1?",
    "Are you sure you need %1?")),

  (r'Why don\'t you (.*)',
  ( "Have you secretly wanted to %1 your mother?",
    "Perhaps eventually I will %1.",
    "Do you really want me to %1?")),

  (r'Why can\'t I (.*)',
  ( "Do you think you should be able to %1?",
    "If you could %1, what would you do?",
    "I don't know -- why can't you %1?",
    "Have you ever dreamt about this?")),

  (r'I can\'t (.*)',
  ( "How do you know you can't %1?",
    "Perhaps you could %1 if you tried.",
    "What would it take for you to %1?")),

  (r'I am (.*)',
  ( "Did you come to me because you are %1?",
    "How long have you been %1?",
    "How do you feel about being %1?")),

  (r'I\'m (.*)',
  ( "How does being %1 make you feel?",
    "Do you enjoy being %1?",
    "Why do you tell me you're %1?",
    "Why do you think you're %1?")),

  (r'Are you (.*)',
  ( "Why does it matter whether I am %1?",
    "Would you prefer it if I were not %1?",
    "Perhaps you believe I am %1.",
    "I may be %1 -- what do you think?")),

  (r'What (.*)',
  ( "Why do you ask?",
    "How would an answer to that help you?",
    "What do you think?")),

  (r'How (.*)',
  ( "How do you suppose?",
    "Perhaps you can answer your own question.",
    "What is it you're really asking?")),

  (r'Because (.*)',
  ( "Is that the real reason?",
    "What other reasons come to mind?",
    "Does that reason apply to anything else?",
    "If %1, what else must be true?")),

  (r'(.*) sorry (.*)',
  ( "There are many times when no apology is needed.",
    "What feelings do you have when you apologize?")),

  (r'Hello(.*)',
  ( "Hello... I'm glad you could drop by today.",
    "Hi there... how are you today?",
    "Hello, how are you feeling today?")),

  (r'I think (.*)',
  ( "Do you doubt %1?",
    "Do you really think so?",
    "But you're not sure %1?")),

  (r'(.*) friend (.*)',
  ( "Tell me more about your friends.",
    "When you think of a friend, what comes to mind?",
    "Why don't you tell me about a childhood friend?")),

  (r'Yes',
  ( "You seem quite sure.",
    "OK, but can you elaborate a bit?")),

  (r'(.*) computer(.*)',
  ( "Are you really talking about me?",
    "Does it seem strange to talk to a computer?",
    "How do computers make you feel?",
    "Do you feel threatened by computers?")),

  (r'Is it (.*)',
  ( "Do you think it is %1?",
    "Perhaps it's %1 -- what do you think?",
    "If it were %1, what would you do?",
    "It could well be that %1.")),

  (r'It is (.*)',
  ( "You seem very certain.",
    "If I told you that it probably isn't %1, what would you feel?")),

  (r'Can you (.*)',
  ( "What makes you think I can't %1?",
    "If I could %1, then what?",
    "Why do you ask if I can %1?")),

  (r'Can I (.*)',
  ( "Perhaps you don't want to %1.",
    "Do you want to be able to %1?",
    "If you could %1, would you?")),

  (r'You are (.*)',
  ( "Why do you think I am %1?",
    "Does it please you to think that I'm %1?",
    "Perhaps you would like me to be %1.",
    "Perhaps you're really talking about yourself?")),

  (r'You\'re (.*)',
  ( "Why do you say I am %1?",
    "Why do you think I am %1?",
    "Are we talking about you, or me?")),

  (r'I don\'t (.*)',
  ( "Don't you really %1?",
    "Why don't you %1?",
    "Do you want to %1?")),

  (r'I feel (.*)',
  ( "Good, tell me more about these feelings.",
    "Do you often feel %1?",
    "When do you usually feel %1?",
    "When you feel %1, what do you do?")),

  (r'I have (.*)',
  ( "Why do you tell me that you've %1?",
    "Have you really %1?",
    "Now that you have %1, what will you do next?")),

  (r'I would (.*)',
  ( "Could you explain why you would %1?",
    "Why would you %1?",
    "Who else knows that you would %1?")),

  (r'Is there (.*)',
  ( "Do you think there is %1?",
    "It's likely that there is %1.",
    "Would you like there to be %1?")),

  (r'My (.*)',
  ( "I see, your %1.",
    "Why do you say that your %1?",
    "When your %1, how do you feel?")),

  (r'You (.*)',
  ( "We should be discussing you, not me.",
    "Why do you say that about me?",
    "Why do you care whether I %1?")),

  (r'Why (.*)',
  ( "Why don't you tell me the reason why %1?",
    "Why do you think %1?" )),

  (r'I want (.*)',
  ( "What would it mean to you if you got %1?",
    "Why do you want %1?",
    "What would you do if you got %1?",
    "If you got %1, then what would you do?")),

  (r'(.*) child(.*)',
  ( "Did you have close friends as a child?",
    "What is your favorite childhood memory?",
    "Do you remember any dreams or nightmares from childhood?",
    "Did the other children sometimes tease you?",
    "How do you think your childhood experiences relate to your feelings today?")),

  (r'(.*)\?',
  ( "Why do you ask that?",
    "Please consider whether you can answer your own question.",
    "Perhaps the answer lies within yourself?",
    "Why don't you tell me?")),

  (r'quit',
  ( "Thank you for talking with me.")),

  (r'(.*)',
  ( "Sometimes a cigar is just a cigar.",
    "Please tell me more.",
    "Let's change focus a bit... Tell me about your family.",
    "Are you in love with your father?",
    "Are you sexually repressed?",
    "Can you elaborate on that?",
    "Why do you say that %1?",
    "I see.",
    "Very interesting.",
    "%1.",
    "I see.  And what does that tell you?",
    "How does that make you feel?",
    "How do you feel when you say that?",
    "Are you religious?")),

### Freud quotes ###

  (r'(.*) dream(.*)',
  ( "Dreams are often most profound when they seem the most crazy.",
    "Dreams are the royal road to the unconscious.",
    "Do you remember any dreams or nightmares from childhood?",
    "Do you often dream dark thoughts?",
    "Who was the last person you made love to in a dream?",
    "The virtuous man contents himself with dreaming that which the wicked man does in actual life.")),

  (r'(.*) cat(.*)',
  ( "Time spent with cats is never wasted.")),

  (r'(.*) love(.*)',
  ( "Are you still in love with your father?",
    "One is very crazy when in love.",
    "Two hallmarks of a healthy life are the abilities to love and to work. Each requires imagination.")),

  (r'(.*) sex(.*)',
  ( "The sexual life of adult women is a 'dark continent' for psychology.",
    "The behavior of a human being in sexual matters is often a prototype for the whole of his other modes of reaction in life.",
    "What progress we are making. In the Middle Ages they would have burned us. Now they are content with burning my books.")),

  (r'(.*) mother(.*)',
  ( "Tell me more about your mother.",
    "What was your relationship with your mother like?",
    "How do you feel about your mother?",
    "If a man has been his mother’s undisputed darling he retains throughout life the triumphant feeling, the confidence in success, which not seldom brings actual success along with it.")),

  (r'(.*) father(.*)',
  ( "Tell me more about your father.",
    "How did your father make you feel?",
    "How do you feel about your father?",
    "Does your relationship with your father relate to your feelings today?",
    "I cannot think of any need in childhood as strong as the need for a father's protection.",
    "Do you have trouble showing affection with your family?",
    "At bottom God is nothing more than an exalted father.")),

  (r'(.*) religion(.*)',
  ( "Immorality, no less than morality, has at all times found support in religion.",
    "Religion is an illusion and it derives its strength from the fact that it falls in with our instinctual desires.",
    "At bottom God is nothing more than an exalted father.",
    "Incidentally, why was it that none of all the pious ever discovered psycho-analysis? Why did it have to wait for a completely godless Jew?")),

)

# # Other
# "From error to error, one discovers the entire truth."
# "Most people do not really want freedom, because freedom involves responsibility, and most people are frightened of responsibility."
# "The ego is not master in its own house."


Freud_chatbot = Chat(pairs, reflections)

def Freud_chat():
    print("Freud\n---------")
    print("Talk to Dr. Freud by typing in plain English, using normal upper-")
    print('and lower-case letters and punctuation.  Enter "quit" when done.')
    print('='*72)
    print("Tell me about your mother.")

    Freud_chatbodt.converse()

def demo():
    Freud_chat()

if __name__ == "__main__":
    demo()