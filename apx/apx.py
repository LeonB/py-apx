import sys
import email
import logging
import logging.handlers

class AttachmentParser(object):

    def get_attachments(self, mail):
        attachments = []
        if mail.is_multipart():
            continue_n = 0
            for part in mail.walk():
                # Dit is dubbelop met het checken van rfc822
                #if continue_n > 0:
                    #    continue_n = continue_n - 1
                    #    continue

                content_disposition = part.get("Content-Disposition", None)
                Logger.getInstance().debug('content_disposition: %s' % content_disposition.__str__())

                if not content_disposition:
                    continue

                dispositions = content_disposition.strip().split(';')
                Logger.getInstance().debug(dispositions[0])
                if (
                    dispositions[0].lower() != 'inline' and
                    dispositions[0].lower() != 'attachment'
                ):
                    continue
                else:
                    attachment = part

                content_type = attachment.get('Content-type').split(';')[0]
                Logger.getInstance().debug('content_type: %s' % content_type)
                if (not content_type == 'message/rfc822'):
                    continue

                if attachment:
                    # Als de attachment zelf attachments heeft: neem die dan mee
                    if attachment.is_multipart():
                        payload = ''
                        for pl in attachment.get_payload():
                            payload = payload + pl.__str__()
                            attachments.append(email.message_from_string(payload))
                            #continue_n = len(attachment.get_payload())
                            continue
                    else:
                        attachments.append(attachment)
                        continue

        return attachments

class StdoutFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR

class Logger(object):
    instance = None

    def __init__(self, **kwargs):
        self.logger = logging.getLogger("apx")
        self.logger.setLevel(logging.DEBUG)

        slh = logging.handlers.SysLogHandler(address='/dev/log')
        slh.setLevel(logging.__getattribute__(kwargs['log_level'].upper()))
        self.logger.addHandler(slh)

        if not kwargs['quiet']:
            she = logging.StreamHandler(sys.stderr)
            she.setLevel(logging.ERROR)
            self.logger.addHandler(she)

            sho = logging.StreamHandler(sys.stdout)
            sho.setLevel(40-kwargs['verbosity']*10)
            sho.addFilter(StdoutFilter())
            self.logger.addHandler(sho)

    @classmethod
    def getInstance(cls):
        return cls.instance

    def debug(self, msg, *args, **kwargs):
        return self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        return self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        return self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        return self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        return self.logger.critical(msg, *args, **kwargs)
