function bkch_periodic_table ()
{
    var frame = bkch_switch_page ("chrome://bkch/content/periodic.xul");
    var focus_element = frame.contentDocument.getElementsByTagName ('description')[0];
    focus_element.focus ();
}
