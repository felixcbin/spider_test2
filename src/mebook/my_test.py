import re

def main():
    key = '<li class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-2021" id="menu-item-2021"><a href="http://mebook.cc/category/cxxs/jdmz">经典名著·社会哲学</a></li>'+'\r\n<li class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-2021" id="menu-item-2021"><a href="http://mebook.cc/category/cxxs/jdmz">经典名著·社会哲学</a></li>'
    key2 = '<div class="thumbnail"><div class="cat"><a href="http://mebook.cc/category/cxxs" rel="category tag">畅销小说</a> · <a href="http://mebook.cc/category/cxxs/jdmz" rel="category tag">经典名著·社会哲学</a></div><div class="img"><a href="http://mebook.cc/28953.html" title="《人的宗教（精制精排）》[美]休斯顿·史密斯（作者）epub+mobi"><img src="http://i2.tiimg.com/621500/718434aa622f00e3t.jpg"/></a></div></div><div class="content"><h2> <a href="http://mebook.cc/28953.html" title="《人的宗教（精制精排）》[美]休斯顿·史密斯（作者）epub+mobi">《人的宗教（精制精排）》[美]休斯顿·史密斯（作者）epub+mobi</a></h2><div class="info"><span class="new">NEW!</span>  2019.06.16 · <a href="http://mebook.cc/28953.html#respond">发表评论</a></div><p>'
    # result = re.findall(r'<a href=(.*?)</a>', key, re.S)
    # print(result)
    # kvs = [(info.split(">")[0][1:-1] ,info.split(">")[1] )for info in result]
    # for kv in kvs:
    #     print(kv[0] + "=" + kv[1])
    result = re.findall(r'<h2>(.*?)</h2>', key2, re.S)
    result = [url.split('"')[1] for url in result]
    print(result)



if __name__ == '__main__':
    main()
