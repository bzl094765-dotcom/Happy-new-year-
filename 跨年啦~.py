import time
import random
import sys
import os
import math

# ========== 可自由替换区（强烈建议你自己改） ==========
# 随机祝福语
RANDOM_MESSAGES = [
    "新的一年，新的 Bug。",
    "Hello 2026!",
    "愿代码无 Bug，生活无 Null (空虚)。",
    # #### 1. 对长辈
    "红马送福来，愿您龙马精神永不减，福寿安康岁岁甜！",
    "新春策马迎新岁，祝您身体如骏马般硬朗，日子如蜜糖般香甜。",
    "马踏祥云添福寿，愿您新岁笑口常开，儿孙绕膝乐融融。",
    # #### 2. 对亲友
    "骏马奔腾开新局，祝你财运如马蹄声声，步步来，日子事事顺。",
    "马年并肩向前跑，愿我们的情谊越走越近，岁岁年年常相伴。",
    "马蹄哒哒报春来，愿你兜里有钱、身边有伴、心里有光，平安顺遂。",
    # #### 3. 对同事 / 领导
    "马年策马扬鞭，愿你职场驰骋四方，业绩一路开挂，前程光芒万丈。",
    "一马当先启新程，祝我们携手共进，新岁再创佳绩、皆得所愿。",
    "马到成功展宏图，愿你工作顺心、晋升有盼，职场之路越走越宽。",
    # #### 4. 对晚辈
    "以梦为马，不负韶华，愿你少年意气，乘风破浪，未来皆可期。",
    "马年如小马驹般朝气，愿你眼里有光，脚下有路，勇敢奔赴热爱。",
    "骏马奔腾向未来，祝你学业突飞猛进，每一步都走得稳稳当当。",
    # #### 5. 通用幽默款
    "“马” 上发财，钱包 “马” 上膨胀，数钱数到手抽筋！",
    "告别摸鱼，“马” 上翻身，今年主打一个稳赢！",
    "红马送好运，offer “马” 上到，加薪 “马” 上成！"
]

# 对联
COUPLETS = {
    "喜庆": [
        ("春风送暖千家福", "瑞雪迎新万象兴", "新春大吉"),
        ("岁启新元百事顺", "年添锦绣万家欢", "万事如意"),
    ],
    "学业": [
        ("灯下苦读三更月", "笔下生花万里程", "金榜题名"),
    ],
    "事业": [
        ("一帆风顺年年好", "万事如意步步高", "五福临门"),
    ],
    "幽默风趣": [
        ("旧岁烦恼全清零", "新年快乐满格充", "元气爆棚"),
        ("干饭追剧无烦恼", "暴富脱单不迟到", "心想事成"),
        ("去年立下的flag倒一片", "今年目标咱主打一个稳", "慢慢来赢"),
        ("旧岁摸鱼全清零", "红马踏春“马”上赢", "一马当先"),
        ("去年flag倒满地", "今岁骏马带财来", "马到功成"),
        ("奶茶自由不用等", "暴富脱单“马”上成", "心想事成"),
    ],
    "温暖感动": [
        ("家人闲坐灯火可亲", "新年伊始喜乐安宁", "岁岁平安"),
        ("旧年风雨皆同舟", "新岁暖阳共携手", "人间值得"),
        ("三餐四季温柔以待", "万水千山好运常在", "顺遂无忧"),
        ("红马踏春送暖意", "阖家团圆享安宁", "岁岁安康"),
        ("旧年风雨皆相伴", "马岁暖阳共相守", "人间值得"),
        ("马蹄声声传吉语", "亲友常伴乐无忧", "喜乐绵长"),
    ],
    "清远悠长": [
        ("旧岁千般皆如意", "新年万事定称心", "时和岁好"),
        ("雪落梅开迎新岁", "风清月朗贺丰年", "春满人间"),
        ("辞旧岁山河锦绣", "迎新年岁月峥嵘", "国泰民安"),
        ("红马迎春开新局", "山河锦绣启丰年", "时和岁好"),
        ("辞旧岁风调雨顺", "迎马年国泰民安", "春满人间"),
        ("骏马奔腾踏福至", "岁安人和万事兴", "福禄绵长"),
    ]
}

WISH_OPTIONS = [
    "身体健康",
    "学业进步",
    "财富自由",
    "隐藏选项·天命之光"
]

COMMON_BLESSINGS = [
    "新年快乐，万事顺遂！",
    "愿你所求皆如愿，所行皆坦途。",
    "愿新年胜旧年。",
    # ### 幽默风趣类关键词扩展祝福语
    "暴富：新的一年，钱包鼓鼓，暴富暴富，数钱数到手抽筋！",
    "脱单：跨年钟声一响，桃花朵朵开，脱单好运来，有人陪你吃火锅！",
    "元气满满：旧岁烦恼清零，新年元气拉满，干啥都顺，干啥都飒！",
    "flag 不倒：今年立下的 flag，个个坚挺不翻车，目标全部能实现！",
    "干饭自由：新岁干饭不打烊，想吃啥就吃啥，体重还能悄悄降！",
    # ### 温暖感动类关键词扩展祝福语
    "阖家安康：新年灯火暖，家人常相伴，岁岁皆安康，年年都团圆。",
    "喜乐安宁：旧年的愁绪随风散，新年的喜乐装满院，日日皆安宁，时时有笑颜。",
    "温柔相伴：新的 365 天，有良人相伴，有好友惦念，每一刻都温柔又缱绻。",
    "风雨同舟：感谢旧年并肩的人，新年继续携手，风雨同舟，万事皆不愁。",
    "好运常在：新岁开门迎好运，出门遇贵人，干啥都顺心，好运天天在！",
    # ### 清远悠长类关键词扩展祝福语
    "岁安人和：雪落迎新年，山河皆无恙，岁安人和睦，日子有清香。",
    "山河锦绣：辞旧岁看山河锦绣，迎新年赏人间烟火，岁岁皆胜意。",
    "万事称心：新的一年，所求皆如愿，所行皆坦途，万事都称心。",
    "梅开岁暖：梅开枝头迎岁暖，风拂人间送春来，新岁多欢喜。",
    "时和年丰：风调雨顺时和岁，五谷丰登人安乐，新年岁岁好风光。",
]

IDIOMS = [
    "一帆风顺", "心想事成", "前程似锦", "万事胜意"
]

# 默认一次性展示条数
DEFAULT_DISPLAY_COUNT = 4

# ===================================================
# 清屏函数
def clear():
    os.system("cls" if os.name == "nt" else "clear")        # 清屏
# 打字机效果
def particle_text(text):
    for ch in text:
        print(ch, end="", flush=True)                       # 打字机效果
        time.sleep(0.2)
    print()
# 倒计时
def countdown(seconds=5):
    for i in range(seconds, 0, -1):
        print(f"跨年倒计时：{i} 秒", end="\r")
        time.sleep(1)
    print("\n🎉 新年到啦！")
# 显示进度条
def show_progress(duration=1.314, desc="加载中"):
    try:
        from tqdm import tqdm
        steps = 100
        for _ in tqdm(range(steps), desc=desc, ncols=60):
            time.sleep(duration/steps)
    except Exception:
        start = time.time()
        while time.time() - start < duration:
            elapsed = time.time() - start
            width = 30      # 不包含前面的文字等
            ratio = min(1.0, elapsed / duration)
            filled = int(ratio * width)
            bar = ("█" * filled) + ("-" * (width - filled))
            print(f"{desc} [{bar}] {int(ratio*100)}%", end="\r")    # end="\r"表示不换行，覆盖当前行
            time.sleep(0.03)
        print(f"{desc} [{'█'*30}] 100%")

# 设置matplotlib中文和负号显示问题
def configure_matplotlib():
    pass

# 显示ASCII艺术图案
def show_ascii_2026():
    show_progress(0.71828, "加载 ASCII 2026")
    print(" ████████████████████████")
    print(" ASCII 艺语！")
    ascii_2026 = r"""
 ██████╗  ██████╗ ██████╗  ██████╗
╚════██╗██╔═████╗╚════██╗██╔════╝
 █████╔╝██║██╔██║ █████╔╝███████╗
██╔═══╝ ████╔╝██║██╔═══╝ ██╔═══██╗
███████╗╚██████╔╝███████╗╚██████╔╝
╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝
"""
    print(ascii_2026)
    print("✨ 新年快乐 🎉 ✨")

# 随机窗口消息
def random_window_message():
    try:
        # 让用户选择要显示多少条祝福语
        try:
            cnt_in = input(f"请选择您的祈福次数（回车默认{DEFAULT_DISPLAY_COUNT}）：")
            cnt = int(cnt_in) if cnt_in.strip() else DEFAULT_DISPLAY_COUNT
        except Exception:
            cnt = DEFAULT_DISPLAY_COUNT

        if not RANDOM_MESSAGES:
            msg = "Hello 2026"
            sample_count = 1
        else:
            sample_count = max(1, min(len(RANDOM_MESSAGES), cnt))
            if sample_count == 1:
                msgs = [random.choice(RANDOM_MESSAGES)]
                msg = msgs[0] + "\n\n愿这份祝福如星光般照亮你的新岁~"
            else:
                msgs = random.sample(RANDOM_MESSAGES, sample_count)
                # 为多条祝福添加生动连接词
                connectors = ["紧接着，", "还有哦~", "悄悄告诉你，", "对了对了，", "最后呀，"]
                msg_parts = [msgs[0]]
                for i in range(1, len(msgs)):
                    conn = connectors[i % len(connectors)]
                    msg_parts.append(f"{conn}{msgs[i]}")
                msg = "\n\n".join(msg_parts) + "\n\n这么多祝福，总有一款适合你！"
        
        print("\n" + "="*30)
        print(msg)
        print("="*30 + "\n")
    except Exception as e:
        print(f"（出错: {e}，跳过展示）")

# 随机对联
def choose_couplet():
    print("请选择你想生成的对联类型：")
    
    # 随机选择 3 组供选择（如果不足3组则全选）
    keys = list(COUPLETS.keys())
    if len(keys) > 3:
        display_keys = random.sample(keys, 3)
    else:
        display_keys = keys
        
    for i, k in enumerate(display_keys, 1):
        print(f"{i}. {k}")
        
    choice = input("输入编号：")

    try:
        selected_key = display_keys[int(choice) - 1]
    except:
        selected_key = display_keys[0]

    # 允许用户指定生成几组对联，默认4组
    try:
        cnt_in = input("请选择您生成的对联数（回车默认4）：")
        cnt = int(cnt_in) if cnt_in.strip() else 4
    except Exception:
        cnt = 4

    pool = COUPLETS[selected_key]
    sample_count = max(1, min(len(pool), cnt))
    if sample_count == 1:
        samples = [random.choice(pool)]
    else:
        samples = random.sample(pool, sample_count)

    # 简单的居中对齐展示，增加生动提示
    width = 60
    print("\n生成的对联来啦~ 每一副都藏着好运哦：\n")
    for idx, (up, down, mid) in enumerate(samples, 1):
        if sample_count > 1:
            print(f"---- 第 {idx} 副闪亮登场 ----")
        print(f"   {mid}   ".center(width))
        print(f"{up}   {down}".center(width))
        if idx < sample_count:
            print("\n✨ 换一副更精彩的 ✨\n")
        else:
            print("\n🎉 对联大放送完毕 🎉")

    time.sleep(1.314)

# 生成Wishing
def make_wish():
    print("\n请许下您的新年愿望：")
    for i, w in enumerate(WISH_OPTIONS, 1):
        print(f"{i}. {w}")

    choice = input("请选择：")
    try:
        wish = WISH_OPTIONS[int(choice) - 1]
    except:
        wish = WISH_OPTIONS[0]

    # 统一定义，避免作用域错误
    food_list = """您今年会吃到————
蒸马脯、蒸马腱、蒸马尾儿，烧马排、烧马腿、烧马块儿，
卤马肉、酱马肉、熏马肠、马肉腊肉、松花马肉卷、马肉小肚儿、
晾马肉、风干马肠，什锦马肉苏盘、熏马肋、白肚马肉卷、
清蒸八宝马肉、江米酿马肉，罐儿焖马腩、罐儿煨马腱、
卤什锦马肉、酱马肘、卤马舌、烩马肚、炝马板筋儿，
马里脊、马腿肉、马肉菜蟒、马肉鱼丸、清蒸马肉哈什蚂，
烩马腰儿、烩马条儿、清拌马丝儿、马心管儿，焖马腩、
红烧马肉、豆豉焖马肉、锅烧马排、烀皮马肉、锅烧马块、
抓炒马柳，软炸马里脊、软炸马排、什锦马肉套肠、麻酥马肉卷儿，
熘马肉鲜蘑、熘马脯儿、熘马鱼片儿、熘马肚儿、醋熘马肉片儿，
烩马肉三鲜、烩马肉白蘑、烩马肉鸽子蛋、炒马肉丝、
红马年压轴硬菜：
【龙马精神马肉大盘鸡】、【马到成功红烧马排】、
【福禄绵长炖马肉大鹅】、【一马当先香酥马腿】！
祝新岁吃嘛嘛香、龙马精神、万事顺遂！
"""

    if "隐藏" in wish:
        print("\n！！！触发隐藏的天命之光！！！")
        print(food_list)

        # 隐藏选项时多给出几条成语（最多 4 条）
        idiom_count = min(4, len(IDIOMS))
        idioms = random.sample(IDIOMS, idiom_count)
        print("并得到：" + "、".join(idioms))
        print("🎁 获得派蒙小精灵一只！")
        time.sleep(1.314)

    else:
        print(f"\n你的愿望是：{wish}")
        print(" 可恶！ 居然不选天命之光！！😈")
        print("🌟 愿望已收录，正在派送好运中... 🌟")
        time.sleep(1.314)

        try:
            import matplotlib.pyplot as plt
            configure_matplotlib()
            fig = plt.figure(figsize=(10, 8))
            plt.text(0.5, 0.5, food_list, fontsize=10, ha='center', va='center', wrap=True)
            plt.axis('off')
            plt.show(block=False)
            plt.pause(3)
            plt.close(fig)
        except Exception:
            print(food_list)  # 降级输出

# 彩蛋
def easter_egg():
    show_progress(1.314, "加载彩蛋")
    try:
        import matplotlib.pyplot as plt
        configure_matplotlib()
        text_content = r"""H. Sora与旮旯给木

        time limit per test
        1 s

        memory limit per test
        256 megabytes

        **以下全是出题人发癫，题目正文往下翻**

        你为啥跟我直接表白啊?! 嘎啦game里不是这样!你应该多跟我聊天，然后提升我的好感度。
        偶尔给我送送礼物，然后在那个特殊节日时候跟我有特殊互动。最后在某个我内心神秘事件中，
        向我表白，我同意跟你在一起，然后我给你看我的特殊CG啊。你怎么直接上来跟我表白!?
        嘎啦game里根本不是这样!我不接受!!

        什么叫我跟很多人搞暧昧啊galgame里就是这样我单身你也单身他们都是单身他们都是可攻略角色
        我当然可以和他们聊天了那如果最后每一个人我都聊失败了这不是更可怜吗再说了我连你对我的好
        感度有多少我都不知道我还没开始玩你这条支线呐你先排队吧好不好什么叫只可以跟你聊天啊你
        这个人怎么这么自私我不跟你聊了!!!

        galgame里刷好感度不应该都是这么刷的吗?? 我和你聊天开心了好感度嘎嘎往上涨，我每次跟
        你聊天你都嘎嘎乐啊，你跟我畅聊这么久，结果你今天给我分享个男的说你爱上他了，不是凭啥啊，
        galgame里根本不是这样的，你俩初始好感度应该是0，我跟你聊这么久，我跟你好感度应该早就
        满了，不是应该你向我表白吗?你怎么说喜欢那个男的啊

        把我挂在网上很正常啊，因为我是高人气角色，我是人气王，大家都想攻略我，又没有我的攻略手段，
        就有好心人出来给大家答疑解惑了。嘎啦game的，唉!是不是这样啊?没办法。魅力值高就是这
        样子的。什么叫我特殊CG也给挂出来了?

        我现在禁止任何人跟我聊天！！因为你想一下，我的智商也很高，我的情商也很高而且我在旮旯game
        里面与上百位美少女谈过恋爱，掌握数百种攻略方案，假如对面没什么恋爱经验的话，会比较单
        纯，跟我聊几句话，两三天直接就爱上我了，那我怎么办，我到时候怎么办，你爱我爱的死去活来的，
        我瞬间伤了你的心

        **以上全是出题人发癫，从这里开始才是题目**

        Sora想要成为Galgame大师，于是开始到处收集Galgame。有的Galgame会给Sora带来愉悦，
        但有的Galgame则会让Sora非常难受。

        现在Sora手上有 n 部Galgame，第 i 部Galgame的愉悦值为 ai。Sora在玩Galgame时会有一个
        心情值 k。当Sora玩到第 i 部Galgame时，若 ai ≥ k ，则 k 会加一；反之，若 ai < k ，
        则 k 会减一。开始时Sora的心情值为 0 。请你为Sora安排一下游玩顺序，让Sora心情值能够达到
        最高，告诉Sora他的心情值最高能是多少。

        Input
        第一行一个整数 n（ 1 ≤  n ≤  10^4 ），表示Galgame的数量。
        第二行 n 个数，第 i 个数为 ai（ 0 ≤  |ai| ≤  10^9 ），表示这部Galgame的愉悦值。

        Output
        输出一行一个整数，表示Sora最后能够到达的最高心情值。

        Example
        Input
        5
        -1 3 0 2 1

        Output
        3

        Note
        Sora可以按 {3,-1,0,1,2} 的顺序玩，最后能够得到 3，且不存在任何一种排列能够得到比这更高的结果。
        """
        fig = plt.figure(figsize=(10, 8))
        plt.text(0.01, 0.99, text_content, fontsize=8, ha='left', va='top')
        plt.axis('off')
        plt.show(block=False)
        plt.pause(2.71828) # 稍微展示几秒以便看清（虽然题目说快速，但太快就看不见了）
        plt.close(fig)
    except:
        print("\n（matplotlib 未启用，直接输出彩蛋文本）\n")
        # 如果没有 matplotlib，直接打印
        print("{ 出题人发癫内容加载中…… }")
        time.sleep(1)
        print("……（省略若干情绪化独白）……") # 这里简化输出，或者你可以把整段文本 print 出来

    print("“出题人”撤回了一条消息，并坏笑了一下 😈")

def main():
    clear()
    # 1. 跨年倒计时
    countdown()
    # 2. 粒子文字 + ASCII 2026
    particle_text("新 年 快 乐 🎉")
    show_ascii_2026()
    # 3. 随机窗口展示
    random_window_message()
    # 4. 选择对联
    choose_couplet()
    # 5. 许愿
    make_wish()
    # 6. 常用祝福语
    print("\n新年祝福语~（每条都藏着小温暖哦）：")
    for i, b in enumerate(COMMON_BLESSINGS, 1):
        print(f"· {i}. {b}")
        if i % 3 == 0 and i != len(COMMON_BLESSINGS):  # 每3条加个分隔，增加节奏感
            print("  ┄┄┄┄┄ 福气分割线 ┄┄┄┄┄")
    # 7. 彩蛋（发癫题目）
    easter_egg()
    # 8. 保存祈福
    save = input("\n是否保存此次祈福（y/n）：")
    if save.lower() == 'y':
        print("✨ 祈福已保存，愿好运常伴你 ✨")
    else:
        print("祝你元旦快乐，新年顺遂！🎆")
    
    input("\n按回车键退出程序...")

if __name__ == "__main__":
    main()