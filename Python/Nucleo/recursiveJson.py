class ConvertDictToText:
    def __init__(self):
        pass
    
    def convert(self,json,fileName = "Json.txt"):
        content = self.convertInner(json)
        f = open(fileName,"w")
        f.write(content)
        f.close()

    def convertInner(self,json):
        htmlText = []
        for key,value in json.items():
            if(isinstance(value,dict)):
                if(type(key) == str):
                    htmlText.append("%s" % key)
                    htmlText.append('\n')
                else:
                    htmlText.append('\t')
                    htmlText.append("%s" % key.name)
                    htmlText.append('\n')
                htmlText.append(self.convertInner(value))
            else:
                if(isinstance(value,int)):
                    htmlText.append('\t\t')
                    htmlText.append("%s:%s" % (key,value))
                    htmlText.append('\n')
                elif(isinstance(value,str)):
                    htmlText.append('\t\t')
                    htmlText.append("%s:%s" % (key,value))
                    htmlText.append('\n')
        return "".join(htmlText)

#ConvertDictToText = ConvertDictToText()
#ConvertDictToText.convert(json)