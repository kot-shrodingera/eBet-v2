get_element = '''
async (
    selector,
    rejectTime,
    emptyTextAllowed = true,
    context = document,
) => {
    return new Promise((resolve /* , reject */) => {
        let element = context.querySelector(selector);
        if (element) {
            const elementText = element.textContent.trim();
            if (emptyTextAllowed || elementText !== '') {
                resolve(element);
                return;
            }
        }
        if (rejectTime == 0) {
            resolve(element);
            return;
        }
        const observerConfig = { childList: true, subtree: true, attributes: true };

        const mutationObserver = new MutationObserver((mutations, observer) => {
            element = context.querySelector(selector);
            if (element) {
                const elementText = element.textContent.trim();
                if (emptyTextAllowed || elementText !== '') {
                    resolve(element);
                    observer.disconnect();
                }
            }
        });

        if (rejectTime > 0) {
            window.setTimeout(() => {
                if (element === null) {
                resolve(element);
                mutationObserver.disconnect();
                }
            }, rejectTime);
        }

        mutationObserver.observe(context, observerConfig);
    });
}
'''