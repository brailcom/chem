function bkch_display_error (message)
{
    bkch_switch_page ("chrome://bkch/content/error.xul");
    var frame = document.getElementById ("bkch-frame");
    bkch_run_timer (function () { return bkch_update_error (frame, message); });
}

function bkch_update_error (frame, message)
{
    var document = frame.contentDocument;
    var description_element = document.getElementById ('error-description');
    if (! description_element)
        return false;
    description_element.setAttribute ('value', message);
    return true;    
}
