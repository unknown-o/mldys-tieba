from bs4 import BeautifulSoup
import json,os,time


def getFileList(fileList, path, originalPath):
    dataArr = os.listdir(f"{originalPath}{path}")
    for data in dataArr:
        if(os.path.isdir(f"{originalPath}{path}/{data}")):
            fileList.extend(getFileList([], f"{path}/{data}", originalPath))
        else:
            fileList.append(f"{path}/{data}")
    return fileList

def getTiebaContent(filepath):
    with open(f"{filepath}/page-source.html","r",encoding="utf-8") as f:
        full=True
        htmlC = f.read()
        soup = BeautifulSoup(htmlC, "html.parser")
        replyList = soup.find_all(class_="j_l_post")
        resultList = []
        for item in replyList:
            #楼主名称
            dName = item.find(class_="d_name").find("a").text
            #楼内内容
            item.find("cc").find("div").decompose()
            dContent = item.find("cc").text.strip()

            dTime = item.find(class_="post-tail-wrap").find_all(class_="tail-info")[-1].text
            dCount = item.find(class_="post-tail-wrap").find_all(class_="tail-info")[-2].text

            dReply = []
            for item1 in item.find("ul",class_="j_lzl_m_w"):
                try:
                    if("total_num" in item1['data-field']):
                        continue
                    dRName = json.loads(item1['data-field'].replace('\'','"'))['showname']
                    dRContent = item1.find("span").text
                    dRDatetime = item1.find_all("span")[-1].text
                    dReply.append({
                        "created_at": dRDatetime,
                        "content": dRContent,
                        "nickname": dRName
                    })
                except:
                    full = False
            resultList.append({
                "created_at": dTime,
                "content": dContent,
                "floor_num": dCount,
                "nickname": dName,
                "reply_list": dReply
            })
        if(soup.find_all(class_="pb_list_pager")[0].find("a")!=None):
            full=False
        pTitle = soup.find("h3").text.strip()
    postData = {
            "title":pTitle,
            "is_full":full,
            "content":resultList,
            "created_at": time.time()
        }
    with open(f"{filepath}/post-data.json","w",encoding="utf-8") as f:
        f.write(json.dumps(postData,ensure_ascii=False))
    print(os.path.basename(filepath))
    summary.append({
        "post_id": os.path.basename(filepath),
        "post_data": postData
    })

summary = []
dir = "E:\\mldys\\all"
filelist = getFileList([],"",dir)
for item in filelist:
    if(os.path.basename(item)=="page-source.html"):
        getTiebaContent(os.path.dirname(f"{dir}/{item}"))
with open(f"{dir}/summary.json","w",encoding="utf-8") as f:
    f.write(json.dumps(summary,ensure_ascii=False))
#print(getFileList([],"","E:\\mldys\\all"))