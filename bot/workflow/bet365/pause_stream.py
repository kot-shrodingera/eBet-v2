from ... import logger
from ...browser import Browser

stream_selector = '.hls-HLSStreamingModule > video'

def pause_stream(browser: Browser) -> None:
    stream = browser.node('Stream', stream_selector, 1, required=False)
    if not stream:
        logger.log('No stream')
        return
    stream_paused = stream.get_property('paused')
    logger.log('Stream Paused: {stream_paused}')
    if stream_paused == 'false':
        return
    browser.crdi.Runtime_callFunctionOn(functionDeclaration='function() { this.paused(); }', objectId=stream.remote_object_id)

