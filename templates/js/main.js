window.addEventListener('resize', setCanvaSize);

function setCanvaSize() {

    var itemSize = 300;     // item default size
    var browser = {};       // browser info
    var itemNumber = {};    // number of items that can fit in the window size

    // Get window's width and height
    browser = {
        width: window.innerWidth || document.body.clientWidth,
        height: window.innerHeight || document.body.clientHeight
    };

    // Calculate how many items can fit in the window's width and height
    itemNumber = {
        width: (Math.ceil(browser.width / itemSize)),
        height: (Math.ceil(browser.height / itemSize))
    };

    // Re-set the item size to fit the page width
    itemSize = browser.width / itemNumber.width;

    // Set thumbnail and cover (img) size
    $(".cover").css( "width", itemSize).css( "height", itemSize);
    $(".card").css( "width", itemSize);
    $(".card-body").css( "width", itemSize);
}
setCanvaSize();