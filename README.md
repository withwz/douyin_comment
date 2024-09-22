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

第二部运行main.py打开无头浏览器后，点到一个视频modal中，再点开评论，这一块没做自动化。<br />
会随机一段时间后点↓箭头&&自动评论。
<img width="1282" alt="image" src="https://github.com/user-attachments/assets/85c4ae33-d7b4-44b4-b048-f9690807eb18">





--- 
^ ⑉・ᴗ・⑉ ૮ ˃感谢支持<br />
<img src="https://github.com/user-attachments/assets/8b12eac8-cb25-435d-b098-bd4de82f8777" width="300" />








