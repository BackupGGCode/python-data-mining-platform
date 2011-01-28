#save materials produced during data-mining
class DmMaterial:
    #dict store term -> id
    termToId = {} 
    #dict store id -> term
    idToTerm = {}
    #dict store term -> how-many-docs-have-term
    termToDocCount = {}
    #dict store class -> how-many-docs-contained
    classToDocCount = {}
