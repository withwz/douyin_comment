import random


comments1 = [
    "人海模式来袭，大家都在享受这个美好的假期！🏖️🌊",
    "全国各大景区人潮涌动，仿佛回到了往日的热闹！🌟🌏",
    "这个假期真是让人惊喜，景区的人气爆棚！💥🏞️",
    "欣喜看到大家走出家门，享受大自然的馈赠！🌳☀️",
    "人山人海的背后，是对美好生活的向往！❤️🥳",
    "这样的热闹让人想起了昔日的繁华，真是令人感动！🌈🎉",
    "人海中，每个人都在为自己的快乐而欢笑！😄🙌",
    "虽然人多，但只要心中有美好，便是风景！🌸🌿",
    "在这个秋天，让我们一起去探索更多的美丽！🍂🚶‍♂️",
    "人潮中，有故事、有回忆，期待与你相遇的每一个瞬间！📸✨",
    "无论人多，快乐总能找到你我！🌟👫",
    "景区的热闹，正是对我们共同努力的最好回报！💪🥇",
    "人山人海，让我们更加珍惜这份美好！💖🌍",
    "期待与大家共享更多的风景和快乐时光！🎈🏕️",
    "在这热闹的时刻，记得保护好自己和他人的安全！🚨⚠️",
    "每个人的笑声都是这个假期最美的旋律！🎶🎉",
    "这样的景象，真是说明了我们对生活的热爱！🔥🥳",
    "在假期中，不妨停下脚步，享受这一刻的宁静！🌅🌼",
    "让我们一起创造难忘的回忆，在人海中舞动吧！🕺💃",
    "这个假期，风景虽美，人更美，心更暖！🥰🏞️",
    "人海中，情感的交流从未停歇，让我们彼此温暖！💞🌊",
]
goto_page1 = "https://www.douyin.com/search/%E5%85%A8%E5%9B%BD%E5%A4%9A%E5%9C%B0%E6%99%AF%E5%8C%BA%E5%BC%80%E5%90%AF%E4%BA%BA%E6%B5%B7%E6%A8%A1%E5%BC%8F"


comments2 = [
    "75年来，中国在风雨中崛起，展示了不屈的精神和无限的可能性！🇨🇳✨",
    "新中国的历程是奋斗的篇章，亿万人民携手共筑繁荣之路！💪🌟",
    "从一穷二白到繁荣富强，75年间的每一步都是历史的见证！📈📚",
    "历史在不断书写，新的辉煌正等待我们去创造！🚀🖊️",
    "新中国的成立，开启了民族复兴的新征程，让我们一起铭记这一伟大的时刻！🎉🕊️",
    "在75年间，祖国的每一个角落都在蜕变，我们共同见证了这段光辉岁月！🌈🌍",
    "经济腾飞、科技创新，75年来的成就让世界刮目相看！🔍💡",
    "新中国是我们共同的骄傲，铭记历史，展望未来！🌠🗺️",
    "我们的祖国正以崭新的姿态屹立于世界民族之林！🌳💖",
    "每一位为新中国发展贡献力量的人，都是历史的英雄！🏅👩‍🔧",
    "从长征到现代化建设，奋斗的精神永远铭刻在心！🛤️✊",
    "新中国的75年，是一部波澜壮阔的史诗！让我们传承这份荣耀！📖🎶",
    "在历史的长河中，新时代的中国更加自信、开放和包容！🌊🌏",
    "伟大的中国梦在75年的奋斗中逐渐实现，让我们继续努力！🌟🏆",
    "75年的光辉历程，见证了中华民族的伟大复兴！让我们携手同行！🤝🌻",
    "中国人民用智慧和汗水谱写了一曲不朽的奋斗之歌！🎶✍️",
    "让我们铭记过去，展望未来，为建设更加美好的明天而奋斗！🌅💫",
    "75年间，中国在世界舞台上越来越闪耀，我们自豪地说：我是中国人！🎇❤️",
    "从革命斗争到改革开放，历史的每一页都铭刻着奋斗的印记！📜🚩",
    "新时代的中国，正在不断书写新的辉煌篇章，让我们共同期待！📖✨",
    "在这个特别的时刻，感恩为祖国发展奉献的每一位英雄！🙌🇨🇳",
]
goto_page2 = "https://www.douyin.com/search/%E6%96%B0%E4%B8%AD%E5%9B%BD75%E5%B9%B4%E6%9D%A5%E7%9A%84%E5%85%89%E8%BE%89%E5%8E%86%E7%A8%8B"


comment_tasks = [
    {"comments_list": comments1, "goto_page": goto_page1},
    {"comments_list": comments2, "goto_page": goto_page2},
]


def get_random_caption(list):
    """每次调用返回一个随机的抖音标题"""
    return random.choice(list)


if __name__ == "__main__":
    for _ in range(5):
        print(get_random_caption(comments1))
