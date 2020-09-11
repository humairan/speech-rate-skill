from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import LOG
from mycroft.messagebus.message import Message


class SpeechRate(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.fastest = '0.1'
        self.fast = "0.5"
        self.default = self.normal = '1.0'
        self.slow = '1.5'
        self.slowest = '2.0'
        self.curr_level = 1.0


    @intent_file_handler('increase.rate.intent')
    def handle_level_increase(self, message):
        from mycroft.configuration.config import(
            LocalConf, USER_CONFIG
        )
        new_rate = self.curr_level - 0.10
        if new_rate < 2.0 and new_rate >= 0.1:
            new_config = {
                "tts": {
                    "mimic": {
                        "duration_stretch" : str(new_rate)
                    }
                }
            }
            
            user_config = LocalConf(USER_CONFIG)
            user_config.merge(new_config)
            user_config.store()
            

            self.curr_level = new_rate
            self.bus.emit(Message('configuration.updated'))
            self.speak_dialog('updatedLevel', {'directionChange': 'increased'}) 
        else:
            self.speak_dialog("invalidLevel")


    @intent_file_handler('decrease.rate.intent')
    def handle_level_decrease(self, message):
        from mycroft.configuration.config import(
            LocalConf, USER_CONFIG
        )
        new_rate = self.curr_level + 0.10
        if new_rate <= 2.0 and new_rate > 0.1:
            new_config = {
                "tts": {
                    "mimic": {
                        "duration_stretch" : str(new_rate)
                    }
                }
            }
            user_config = LocalConf(USER_CONFIG)
            user_config.merge(new_config)
            user_config.store()

            self.curr_level = new_rate
            self.bus.emit(Message('configuration.updated'))
            self.speak_dialog('updatedLevel', {'directionChange': 'decreased'})
        else:
            self.speak_dialog("invalidLevel")


    @intent_file_handler('rate.speech.intent')
    def handle_rate_speech(self, message):
        from mycroft.configuration.config import(
            LocalConf, Configuration, USER_CONFIG
        )
        user_config = LocalConf(USER_CONFIG)
        LOG.info(str(user_config))

        user_level = message.data.get('ratelevel')
        LOG.info(user_level)
        rate_var = self.get_rate_var(user_level)

        if(rate_var == "error"):
            self.speak_dialog("invalidInput", {'userLevel': user_level})
        else:
            new_config = {
                "tts": {
                    "mimic": {
                        "duration_stretch" : str(rate_var)
                    }
                }
            }
            user_config.merge(new_config)
            user_config.store()

            LOG.info(str(LocalConf(USER_CONFIG)))
            self.bus.emit(Message('configuration.updated'))
            self.speak_dialog("rate.speech", {'rateLevel': user_level})

    def get_rate_var(self, level):
        if(level == "fastest"):
            self.curr_level = float(self.fastest)
            return self.fastest
        elif(level == "fast"):
            self.curr_level = float(self.fast)
            return self.fast
        elif(level == "normal" or level == "default"):
            self.curr_level = float(self.normal)
            return self.normal
        elif(level == "slow"):
            self.curr_level = float(self.slow)
            return self.slow
        elif(level == "slowest"):
            self.curr_level = float(self.slowest)
            return self.slowest
        else:
            return "error"

def create_skill():
    return SpeechRate()

