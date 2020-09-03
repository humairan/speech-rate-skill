from mycroft import MycroftSkill, intent_file_handler


class SpeechRate(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('rate.speech.intent')
    def handle_rate_speech(self, message):
        self.speak_dialog('rate.speech')


def create_skill():
    return SpeechRate()

