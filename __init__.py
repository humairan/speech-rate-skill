from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import LOG

class SpeechRate(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.fastest = '0.2'
        self.fastest = '0.5'
        self.normal = '1.0'
        self.slow = '1.3'
        self.slowest = '1.5'

    @intent_file_handler('rate.speech.intent')
    def handle_rate_speech(self, message):
        from mycroft.configuration.config import(
            LocalConf, Configuration, DEFAULT_CONFIG
        )
        config = Configuration.get()['tts']['mimic']
        new_config = {
            "duration_stretch" : '1.2'
        }
        local_config = LocalConf(DEFAULT_CONFIG)
        pconfig = local_config.get('duration_stretch', new_config)
        LOG.info(DEFAULT_CONFIG)
        LOG.info(str(pconfig))
        local_config.merge(pconfig)
        local_config.store()

        #updated = Configuration.get()['tts']['mimic']
        #self.speak(str(updated))



        #rate = message.data.get('variable')
        #self.speak(str(result))
        #self.speak_dialog('rate.speech', {'variable': rate})
        self.speak("done")

def stop(self):
    pass

def create_skill():
    return SpeechRate()

