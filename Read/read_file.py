# *coding:utf-8 *
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import requests

SCKEY = "165Nlke-27hsRVmoLj_mm3eye1oAsT4xm"
URL = f"https://sctapi.ftqq.com/{SCKEY}.send"


def send_wechat(title, content):
    """
    发送消息到微信
    :param title: 消息标题
    :param content: 消息内容
    """
    params = {
        "title": title,
        "desp": content
    }
    try:
        response = requests.get(URL, params=params)
        if response.json().get("code") == 0:
            print("微信通知发送成功")
        else:
            print("发送失败:", response.text)
    except Exception as e:
        print("请求异常:", str(e))


def scheduled_task():
    """定时任务要执行的操作"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title = "张先生记得打卡下班！"
    content = f"⏰ 张先生记得打卡下班！\n\n当前时间：{current_time}\n这是来自Python的定时通知"
    send_wechat(title, content)


if __name__ == "__main__":
    # 创建调度器
    scheduler = BlockingScheduler()

    # 添加定时任务（这里设置为每天8:30执行）
    scheduler.add_job(
        scheduled_task,
        'cron',
        hour=16,
        minute=15,
        timezone='Asia/Shanghai'
    )

    # 也可以使用间隔触发（例如每60秒执行一次）
    # scheduler.add_job(scheduled_task, 'interval', seconds=60)

    try:
        print("定时任务已启动...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("定时任务已停止")
