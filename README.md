# docker-python-flask_upload
基本流程：上传zip并判断文件格式->解压zip到docker数据卷内->启动容器运行zip内的main.py->在页面上输出结果并在本地备份。
逻辑比较简单，没有完成对解压包内执行文件的灵活处理，目前在代码中写死了，只执行main.py。
## flask-upload
使用flask upload功能，实现在网页上传zip包到本地服务器。
## docker-py
使用docker-py API，启动一个镜像为python:3的容器，在容器中执行zip包中的主执行文件main.py。

### version
Python=3.5
Docker=v17.09-ce
Docker-py API=1.32
OS=Ubuntu16.04

