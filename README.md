# Who-remove-your-star

## Introduction
Hang the program in the background and check the github repository every hour. This program will record the users that give you star and remove star during one hour.

该程序会一小时检查一次您设置的github仓库，要是有好心人点star或者有坏坏的家伙取消star统统都会记在小本本上。

The `./monitor.logstargazers/{user}/{repo}` folder will be created automatically, and the log will be in `monitor.txt`.

该程序会自动创建`./monitor.logstargazers/{user}/{repo}`文件夹来存储数据，日志会保存在`monitor.txt`中(小本本)。


## Usage
We use [https://github.com/xrli-U/MuSc](https://github.com/xrli-U/MuSc) as an example.

使用作者的另一个仓库作为栗子 [https://github.com/xrli-U/MuSc](https://github.com/xrli-U/MuSc)
```
python main.py --user xrli-U --repo MuSc
```
or
```
python main.py --website https://github.com/xrli-U/MuSc
```
We recommend hanging the program in the background.

建议将程序挂在后台，防止电脑一关直接寄掉。
```
nohup python main.py --website https://github.com/xrli-U/MuSc > monitor.log 2>&1 &
```

