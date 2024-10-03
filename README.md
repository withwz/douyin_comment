## 抖音视频自动评论

## 如何使用

```shell
git clone https://github.com/withwz/douyin_comment.git

pip install -r requirements.txt -i https://mirrors.bfsu.edu.cn/pypi/web/simple/

# 安装无头浏览器
playwright install chromium

# 获取登录抖音凭证
python get_cookie.py

python main.py
```

第一步先python get_cookie.py去获取cookie


第二步运行main.py会打开utils/config下goto_page配置的url，自动点击下边推荐的视频，进入自动评论，自动下一个。<br />
url配置可以在抖音中搜索复制url。<br />
<img width="648" alt="image" src="https://github.com/user-attachments/assets/00772528-bf7b-44d4-a389-1a98e7a3e8ab">

配置comment_tasks数组可以轮询执行里边的任务



--- 
^ ⑉・ᴗ・⑉ ૮ ˃感谢支持<br />
<img src="https://github.com/user-attachments/assets/8b12eac8-cb25-435d-b098-bd4de82f8777" width="300" />








