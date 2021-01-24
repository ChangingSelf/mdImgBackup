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
    if not os.path.exists(pathName): os.mkdir(pathName)

    response = requests.get(url)
    img = response.content
   
    
    if fileName == None:
        fileName = re.split(r'[/\\]',url)[-1]
    
    fullPath = os.path.join(pathName,fileName)

    postfix = 1
    while os.path.exists(fullPath):
        # 若文件已经存在，则给文件名加后缀
        temp = fileName.split('.')
        tempFileName = str(temp[-2]) + '({}).'.format(postfix) + str(temp[-1])
        fullPath = os.path.join(pathName,tempFileName)
        postfix += 1

    with open(fullPath,'wb') as f:
        f.write(img)

        print('[{}]已被保存到[{}]'.format(url,fullPath))

def copyImg(fullPath,outputPath):
    with open(fullPath,'rb') as fin:
        content = fin.read()
    with open(outputPath,'wb') as fout:
        fout.write(content)
    

def backupMdImg(inputPath,outputPath):
    '''
    从markdown文件中提取url并下载到本地
    会递归下载子目录
    @param inputPath: markdown文件所在的路径
    @param outputPath: 图片输出路径
    '''
    if not os.path.exists(outputPath): os.mkdir(outputPath)

    for root, dirs, files in os.walk(inputPath):
        for file in files:
            # 遍历文件
            if file.split('.')[-1]!='md': continue # 如果不是markdown文件则跳过
            with open(os.path.join(root,file),'r',encoding='utf-8') as f:
                content = f.read()
                imgs = re.findall(r'!\[(.*?)\]\((.*?)\)',content,re.M | re.S)
            # 得到的imgs格式:[('图片提示信息','图片url')]
            imgOutputPath = os.path.join(outputPath,file.split('.')[-2])
            for img in imgs:
                # 新建文件对应的文件夹用于存放下载的图片
                url = img[1]
                
                if not re.match(r'^https?:/{2}\w.+$', url):
                    # 如果不是url而是本地图片
                    try:
                        copyImg(os.path.join(root,url),os.path.join(imgOutputPath,re.split(r'[/\\]',url)[-1]))
                    except Exception:
                        print('文件[{}]中的图片[{}]无法找到'.format(os.path.join(root,file),url))
                else:
                    downloadImg(url,imgOutputPath)
                    
        
        for dir in dirs:
            fullPath = os.path.join(outputPath,dir)
            if not os.path.exists(fullPath): os.mkdir(fullPath)
            backupMdImg(os.path.join(inputPath,dir),fullPath)
                    

    

if __name__=='__main__':
    # url = 'https://i.loli.net/2020/10/11/dWXwECpg9SGuzZj.png'
    pathName = r'F:\test\_posts'
    # downloadImg(url,pathName)
    backupMdImg(pathName,r'F:\test\images')
