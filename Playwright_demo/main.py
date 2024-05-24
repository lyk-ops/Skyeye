import requests
import json
import base64
from PIL import Image
import io
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import oss2
from datetime import datetime

def capture_screenshot(url):
    # 启动 Playwright 并打开浏览器
    playwright1 = sync_playwright().start()
    run_browser = playwright1.chromium
    browser = run_browser.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    # 设置较大的视口（可选）
    page.set_viewport_size({'width': 1920, 'height': 3300})
    
    page.goto(url, wait_until='networkidle')
    
    # 等待额外的时间以确保动态内容加载
    time.sleep(10)  # 根据实际情况调整等待时间
    
    # 截取整个页面的截图
    page.screenshot(path='a.png', full_page=True)
    
    # 关闭上下文和浏览器
    context.close()
    browser.close()
    
    # 停止 Playwright
    playwright1.stop()

def sendfile(local_file_path):
    # 设置OSS访问密钥信息
    access_key_id = 'LTAI5txxxxxxxxxxxxxxxx'
    access_key_secret = 'j6cxxxxxxxxxxxxxPqGZV4Ikxxxx'
    endpoint = 'oss-cn-shanghai.aliyuncs.com'
    bucket_name = 'xxxxx'
    
    # 创建OSS客户端实例
    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    # 获取当前时间并格式化为字符串，例如 "20230425123456"
    timestamp_str = datetime.now().strftime('%Y%m%d%H%M%S')
    # 定义文件名前缀和后缀
    filename_prefix = 'jiankong/'
    filename_suffix = '.png'
    # 上传本地文件到OSS
    object_key = filename_prefix + timestamp_str + filename_suffix # 上传到OSS后的文件名
    
    # 使用put_object_from_file方法上传文件
    bucket.put_object_from_file(object_key, local_file_path)
    
    # 生成文件的URL地址
    # 假设您的存储桶访问域名是“<bucket_name>.<endpoint>”，这通常是默认情况。
    # 如果您的存储桶设置了自定义域名，请使用那个域名代替。
    # url = f"http://{bucket_name}.{endpoint}/{object_key}"
    # 获取当前时间并格式化为字符串
    current_time = datetime.now().strftime('上午%H点')
    
    print(f"File {local_file_path} has been uploaded to OSS as {object_key}.")
    
    # 钉钉Webhook URL
    dingtalk_webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxx'
    # 阿里云OSS上的图片URL
    oss_image_url = 'http://xxxxxxxxxxx.oss-cn-shanghai.aliyuncs.com/%s' % object_key
    
    # 构建钉钉Markdown消息
    message = {
        "msgtype": "markdown",
        "markdown": {
            "title": "告警",
            "text": f"### {current_time}巡检监控图片已上传\n![图片]({oss_image_url})"
        
        }
    }
    
    # 发送消息到钉钉群聊
    headers = {'Content-Type': 'application/json'}
    response = requests.post(dingtalk_webhook_url, data=json.dumps(message), headers=headers)
    
    # 检查响应结果
    if response.status_code == 200:
        print("消息发送成功")
    else:
        print("消息发送失败，状态码：", response.status_code)
        print(response.text)

capture_screenshot(url="https://jk.hxxxxxxxxx/d/BN8E0KM4z/4-bxxxxxxxxxprod?orgId=1&kiosk")
sendfile(local_file_path='a.png')