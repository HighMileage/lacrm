"Utilities classes for lacrm module"


class BaseLacrmError(Exception):
    """Base Lacrm API Exception"""

    message = u'Unknown error occured. Response content: {content}.'

    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.message.format(content=self.content)

    def __unicode__(self):
        return self.__str__()


class LacrmArgumentError(BaseLacrmError):
    """Unknown argument Lacrm API Exception"""

    message = u'Improperly formatted argument. Response content: {content}.'

    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.message.format(content=self.content)

    def __unicode__(self):
        return self.__str__()
