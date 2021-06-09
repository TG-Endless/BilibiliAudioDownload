# BilibiliAudioDownloader

## 主要功能

输入视频BV号列表，批量下载B站视频中的音频到本地。

## 使用方法
cmd命令行执行 `dist目录`中的`bili.exe`, 或者把dist目录加入到环境变量。
```
bili <下载目录> bvxxxx1 bvxxxx2
```

## Python版本与依赖库

Python 3.7
```
pip3 install requests, urllib, time
pip3 install pyinstaller
```

### 编译
`pyinstaller -n bili -c --onefile main.py`  
`cd dist`


