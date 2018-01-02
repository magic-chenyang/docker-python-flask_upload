# docker-python-flask_upload
基本流程：上传zip并判断文件格式->解压zip到docker数据卷内->启动容器运行zip内的main.py->在页面上输出结果并在本地备份日志。

> 目前使用docker container方式去启动容器，在使用docker service方式启动容器执行时，目前存在部分问题，还在解决中。
> 逻辑比较简单，没有实现对解压包内执行文件的灵活处理，目前在代码中写死了，只执行main.py。后续再完善。
## flask-upload
使用flask upload功能，实现在网页上传zip包到本地服务器。
## docker-py
使用docker-py API，启动一个镜像为python:3的容器，在容器中执行zip包中的主执行文件main.py。

### version
- Python=3.5
- Docker=v17.09-ce
- Docker-py API=1.32
- OS=Ubuntu16.04

1. 首先选择本地文件，然后upload上传。

![Image text](https://github.com/magic-chenyang/docker-python-flask_upload/blob/master/images/1.png)

2. 显示error，表示上传文件格式不允许，需要后退重新选择。

![Image text](https://github.com/magic-chenyang/docker-python-flask_upload/blob/master/images/4.png)

3. 显示上传成功，点击RUN按钮，启动容器执行。

![Image text](https://github.com/magic-chenyang/docker-python-flask_upload/blob/master/images/2.png)


4. 自动跳转到send_code，显示运行结果，正确和错误都会输出。当前显示为正确输出。

![Image text](https://github.com/magic-chenyang/docker-python-flask_upload/blob/master/images/3.png)
