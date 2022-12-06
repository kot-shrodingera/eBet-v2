from ...browser import Browser

def pause_stream(browser: Browser) -> None:
    browser.run_js_function('''
() => {
    if (!window.pauseVideoIntervalID) {
        window.pauseVideoIntervalID = setInterval(() => {
            const stream = document.querySelector('.hls-HLSStreamingModule > video');
            if (stream) {
                console.log('Interval:Stream', stream);
                if (!stream.paused) {
                    console.log('Pausing stream');
                    stream.pause();
                } else {
                    console.log('Stream is paused');
                }
            } else {
                console.log('Interval:Stream', 'No stream');
            }
        }, 1000);
    }
}
''')

