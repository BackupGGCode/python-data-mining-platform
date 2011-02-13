from xml.dom import minidom

class XmlNode:
    mCurNode = None

    def __init__(self, node):
        self.mCurNode = node

    def GetFirstChild(self, name):
        for node in self.mCurNode.childNodes:
            if node.nodeName == name:
                return XmlNode(node)

    def GetChilds(self, name):
        nodes = []
        for node in self.mCurNode.childNodes:
            if node.nodeName == name:
                nodes.append(XmlNode(node))
        return nodes

    def GetName(self):
        return self.mCurNode.nodeName

    def GetValue(self):
        return self.mCurNode.firstChild.data

    @staticmethod
    def FromFile(path):
        return XmlNode(minidom.parse(path).childNodes[0])

if __name__ == "__main__":
    cfg = XmlNode.FromFile("sandbox/test.xml")
    print cfg.GetName()
    print cfg.GetValue()
    cfg1 = cfg.GetFirstChild("hello")
    print cfg1.GetName()
    print cfg1.GetValue()
    cfgs = cfg.GetChilds("world")
    for c in cfgs:
        print c.GetName()
        print c.GetValue()
