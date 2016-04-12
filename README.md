# Inside

![](https://img.shields.io/badge/subject-a_micro_blog_of_my_own-brightgreen.svg?style=flat)

一个迷你博客，使用管理员用户（Group）创建及管理 post, 用户可在 post 下面评论，提供归档页面，数据导入导出功能。

第一次应用之前需要执行 `start-server.sh`，完成用户组及初始用户的创建。
提供超级管理员用户 `admin:password`；管理员用户 `manager:managerpassword` 属于 `Writer` 用户组，可以添加及修改 post；普通用户需要在 `Django Admin` 中手动创建，暂未提供用户注册功能。

前端使用[vue.js](http://vuejs.org/)构建。

requirements:

> Django==1.9.4  
> whitenoise==3.0  
> MySQL-python==1.2.3

其中 `MySQL-python` 可选。

