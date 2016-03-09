from goose import Goose
from goose.text import StopWordsChinese
url = 'http://news.163.com/15/1119/17/B8Q4P44O00015688.html#f=wfocus'
g = Goose({'stopwords_class': StopWordsChinese})
article = g.extract(url=url)
print article.title

