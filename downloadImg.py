'''
将所选文件夹的markdown文件中的图片保存下载到本地
'''
import requests
import re
import os

def downloadImg(url,pathName,fileName=None):
    '''
    @param url: 需要下载的图片的url
    @param pathName: 图片保存路径
    @param fileName: 文件名，默认为链接中的文件名
    '''
    response = requests.get(url)
    img = response.content
    if fileName == None:
        fileName = re.split(r'[/\\]',url)[-1]
    
    fullPath = os.path.join(pathName,fileName)

    postfix = 1
    while os.path.exists(fullPath):
        # 若文件已经存在，则给文件名加后缀
        temp = re.split('.',fileName)
        tempFileName = temp[:-2] + '({})',format(postfix) + temp[-1]
        fullPath = os.path.join(pathName,tempFileName)

    with open(fullPath,'wb') as f:
        f.write(img)

    pass

def extractUrl(pathName):
    pass

if __name__=='__main__':
    url = 'https://i.loli.net/2020/10/11/dWXwECpg9SGuzZj.png'
    pathName = '.'
    downloadImg(url,pathName)