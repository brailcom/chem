"""
This is an experimental client for the chemical server.
It connects to the server, starts new session and sends it
some data.
It shows the structure sent back by the server in a simple tree.
Nodes of the tree that are links to other parts of the tree will
make the selection jump to the linked item when double-clicked
"""


import pygtk
pygtk.require('2.0')
import gtk


def data_to_nice_tree(data, tree, root, dict=None):
    """this function reads the data structure provided by chem_reader
    and creates a tree-like structure from it in the GTK way.
    It creates the output in a user-friendly way - skipping some nodes as
    'views' etc.
    dict is used to keep track of data->tree-row relationship for further
    use, such as link highlighting etc."""
    # create the node for current item
    if hasattr(data, 'value'):
        this = tree.append(root, [data.data_type().description()+": "+str(data.value())])
    else:
        this = tree.append(root, [data.data_type().description()])
    dict[tree.get_path(this)] = data
    # iterate over linked structures
    for attr in ["views"]:
        if hasattr(data, attr):
            for r in getattr(data, attr)():
                data_to_nice_tree(r, tree, this, dict)
    for attr in ["parts"]:
        if hasattr(data, attr):
            for r in getattr(data, attr)():
                data_to_nice_tree(r.target(), tree, this, dict)
    for attr in ["links"]:
        if hasattr(data, attr):
            sub = tree.append(this, [attr])
            for r in getattr(data, attr)():
                data_to_nice_tree(r.target(), tree, sub, dict)
    for attr in ["neighbors"]:
        if hasattr(data, attr):
            sub = tree.append(this, [attr])
            for r in getattr(data, attr)():
                text = r.data_type().description() + " "
                text += r.target().data_type().description()
                if hasattr(r.target(), "value"):
                    text += ": "+str(r.target().value())
                x = tree.append(sub, ["%s" % text])
                dict[tree.get_path(x)] = r


def row_activated(treeview, iter, path, user_data):
    try:
        end = user_data[iter].target()
    except (AttributeError, KeyError):
        return
    key = None
    for k,v in user_data.iteritems():
        if v == end:
            key = k
            break
    if key:
        ts = treeview.get_selection()
        ts.select_path(k)



class BasicTreeViewExample:

    # close the window and quit
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self, data):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Simple PyGTK example of Chem Client")
        self.window.set_size_request(600, 800)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", lambda w: gtk.main_quit())
        # create a TreeStore with one string column to use as the model
        self.treestore = gtk.TreeStore(str)
        item_to_data = {}  # this is the dict storing tree_node->data relationship
        data_to_nice_tree(data, self.treestore, None, dict=item_to_data)
        # create the TreeView using treestore
        self.treeview = gtk.TreeView(self.treestore)
        self.treeview.connect("row-activated", row_activated, item_to_data)
        self.tvcolumn = gtk.TreeViewColumn('Column 0')
        # add tvcolumn to treeview
        self.treeview.append_column(self.tvcolumn)
        # create a CellRendererText to render the data
        self.cell = gtk.CellRendererText()
        # add the cell to the tvcolumn and allow it to expand
        self.tvcolumn.pack_start(self.cell, True)
        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        self.tvcolumn.add_attribute(self.cell, 'text', 0)
        # make it searchable
        self.treeview.set_search_column(0)
        self.window.add(self.treeview)
        self.window.show_all()


if __name__ == "__main__":
    # try to get the SMILES to process from command line or use the default
    import sys
    import os
    if not len(sys.argv) > 1:
        default = "Oc1ccccc1C"
        print "No SMILES given, using the default '%s'" % default
        text = default
        format = "SMILES"
    elif os.path.exists(sys.argv[1]):
        format = "Molfile"
        f = file(sys.argv[1], "r")
        text = f.read()
        f.close()
    else:
        text = sys.argv[1]
        format = "SMILES"        
    # start the pyro machinery
    import Pyro.core, Pyro.naming
    Pyro.core.initClient()
    locator = Pyro.naming.NameServerLocator()
    ns = locator.getNS()
    # ask for an URI
    uri = ns.resolve('server')
    # connect the server object
    server = Pyro.core.getProxyForURI(uri)
    # request a session
    session = server.connect()
    # make the session object process a string
    data = session.process_string(text, format=format)
    # now process the data
    #print data
    tvexample = BasicTreeViewExample(data)
    try:
        gtk.main()
    # disconnect the session
    finally:
        server.disconnect(session.number())
